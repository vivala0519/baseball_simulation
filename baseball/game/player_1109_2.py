from channels.generic.websocket import WebsocketConsumer
from tornado.httpclient import AsyncHTTPClient
import asynchat
import asyncio
from .teamJang import *
from .models import Batter, Pitcher
from .DBprocess import *
from .GameProcess import *
import json
import time


class ChatConsumer(WebsocketConsumer):


    def record_send(self, message):

        self.send(text_data=json.dumps({
            'message': message,

        }))
        
        # 메세지 보내고 0.5초 대기
        time.sleep(1)


    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': '오늘의 야구 경기를 시작하겠습니다!!',
        }))

    def disconnect(self, close_code):
        self.send(text_data=json.dumps({
            'message': close_code
        }))

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # print(text_data)
        # print("==============================")
        # print(message)

        print("====================================================================")
        print(message)
        print("====================================================================")

        process = DBprocess()
        process.getBattersAndPitchers(message)

        home_batters = process.getBatterStat(process.home_batters)
        home_pitchers = process.getPitchersStat(process.home_pitchers)

        away_batters = process.getBatterStat(process.away_batters)
        away_pitchers = process.getPitchersStat(process.away_pitchers)

        print("home_pitchers = ", home_pitchers)
        print("=============================================================")
        print("home_batters = ", home_batters)
        print("=============================================================")
        print("away_pitchers = ", away_pitchers)
        print("=============================================================")
        print("away_batters = ", away_batters)

        self.inning_proc(home_pitchers, home_batters, away_pitchers, away_batters)


    def inning_proc(self, homePitchers, homeBatters, awayPitchers, awayBatters):  # 경기 진행 로직

        game = Game()

        obpBook = game.get_league_obp()

        awayPitcherList = game.set_league_obp_to_player(awayPitchers, obpBook)
        homePitcherList = game.set_league_obp_to_player(homePitchers, obpBook)

        awayBatterList = game.set_league_obp_to_player(awayBatters, obpBook)
        homeBatterList = game.set_league_obp_to_player(homeBatters, obpBook)

        # 타자 리스트에서 선수 교체 시, 사용할 index
        home_hitterIndex = 0
        away_hitterIndex = 0

        home_hitter_num = homeBatterList[home_hitterIndex]  # 홈팀 타자 번호
        away_hitter_num = awayBatterList[away_hitterIndex]  # 어웨이팀 타자 번호
        innings = range(1, 13)  # 이닝(1 ~ 12)
        base = [0, 0, 0]  # 베이스 리스트, [0] = 1루, [1] = 2루, [2] = 3루


        # 0,1,2에 의미 없음
        away_sp = awayPitcherList[0]  # 어웨이팀 선발투수
        away_rp = awayPitcherList[1]  # 어웨이팀 중계투수
        away_cp = awayPitcherList[2]  # 어웨이팀 마무리투수
        away_sp_pitch_count = 0  # 어웨이팀 선발투수 투구 수
        away_rp_pitch_count = 0  # 어웨이팀 중계투수 투구 수
        away_cp_pitch_count = 0  # 어웨이팀 마무리투수 투구 수
        away_sp_scored = 0  # 어웨이팀 선발투수 실점
        away_rp_scored = 0  # 어웨이팀 중계투수 실점
        away_pitcher = away_sp  # 어웨이팀 투수 초기설정은 선발투수


        home_sp = homePitcherList[0]  # 홈팀 선발투수
        home_rp = homePitcherList[1]  # 홈팀 중계투수
        home_cp = homePitcherList[2]  # 홈팀 마무리투수
        home_sp_pitch_count = 0  # 홈팀 선발투수 투구 수
        home_rp_pitch_count = 0  # 홈팀 중계투수 투구 수
        home_cp_pitch_count = 0  # 홈팀 마무리투수 투구 수
        home_sp_scored = 0  # 홈팀 선발투수 실점
        home_rp_scored = 0  # 홈팀 중계투수 실점
        home_pitcher = home_sp  # 홈팀 투수 초기설정은 선발투수

        for inning in innings:  # 9 ~ 12이닝
            for top_and_bottom in range(1, 3):  # 이닝별 초, 말

                if top_and_bottom == 1:  # 이닝 초
                    
                    self.record_send('1회 초 시작')
                    
                    out = 0
                    self.record_send('-----------------'+ str(inning) + '회 초 원정팀 공격 -----------------')

                    game.setStats(away_hitter_num, home_pitcher)

                    while True:  # 3아웃 되는 동안 실행
                        if home_sp_pitch_count > 100 or home_sp_scored > 3:  # 선발투수 투구 수가 100개 초과이거나 3실점 초과일 경우
                            self.record_send(str(inning) + '회 : ' + 'rp로 투수 교체')
                            home_sp_pitch_count = 0
                            home_sp_scored = 0
                            home_pitcher = home_rp
                            game.setStats(away_hitter_num, home_pitcher)

                        if home_pitcher == home_rp and (
                                home_rp_pitch_count > 100 or home_rp_scored > 3):  # 중계투수 투구 수가 100개 초과이거나 3실점 초과일 경우
                            self.record_send(str(inning) + '회 : ' + 'cp로 투수 교체')
                            home_rp_pitch_count = 0
                            home_rp_scored = 0
                            home_pitcher = home_cp
                            game.setStats(away_hitter_num, home_pitcher)

                        if game.main(home_pitcher[7], away_hitter_num[11]):  # 투수 VS 타자가 아웃일 경우
                            o_res = game.out_result()[0]
                            out += 1  # 아웃카운트 추가
                            away_hitterIndex += 1  # 다음타자
                            if away_hitterIndex == 9:  # 9번 타자 다음은 1번 타자
                                away_hitterIndex = 0
                            self.record_send(str(inning) + '회 : ' + str(away_hitterIndex + 1) + '번 타자, ' + str(o_res))
                            if home_pitcher == home_sp:  # 투수가 선발투수일 시 투구 수 추가
                                if o_res == '삼진':
                                    home_sp_pitch_count += game.pitch_count_case_K()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_sp_pitch_count))
                                else:
                                    home_sp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_sp_pitch_count))
                            if home_pitcher == home_rp:  # 투수가 중계투수일 시 투구 수 추가
                                if o_res == '삼진':
                                    home_rp_pitch_count += game.pitch_count_case_K()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_rp_pitch_count))
                                else:
                                    home_rp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_rp_pitch_count))
                            if home_pitcher == home_cp:  # 투수가 마무리투수일 시 투구 수 추가
                                if o_res == '삼진':
                                    home_cp_pitch_count += game.pitch_count_case_K()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_cp_pitch_count))
                                else:
                                    home_cp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_cp_pitch_count))
                            if out == 3:  # 3아웃일 시
                                break
                        else:  # 투수 VS 타자가 안타일 경우
                            res = game.hit_result()[0]
                            if res == '안타':  # 안타일 경우
                                away_hitterIndex += 1  # 타자번호 + 1
                                if away_hitterIndex == 9:  # 9번타자 다음은 1번타자
                                    away_hitterIndex = 0
                                if base == [0, 0, 0]:  # 베이스에 아무도 없을 경우
                                    base[0] = 1  # 주자 1루
                                elif base == [1, 0, 0]:  # 주자가 1루에만 있을 경우
                                    base[1] = 1  # 주자 1, 2루
                                elif base == [1, 1, 0]:  # 주자가 1, 2루에 있을 경우
                                    base[2] = 1  # 주자 만루
                                elif base == [1, 0, 1]:  # 주자가 1, 3루에 있을 경우
                                    base[1] = 1  # 주자 1, 2루,
                                    base[2] = 0
                                    game.away_score += 1  # 어웨이팀 점수 + 1
                                    game.inning_away_score += 1  # 해당이닝 어웨이팀 점수 + 1
                                    if home_pitcher == home_sp:  # 홈팀 투수 선발투수일 경우
                                        home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                    if home_pitcher == home_rp:  # 홈팀 투수 중계투수일 경우
                                        home_rp_scored += 1  # 홈팀 중계투수 실점 + 1
                                elif base == [0, 1, 1]:  # 주자가 2, 3루에 있을 경우
                                    base[0] = 1  # 주자 1, 3루,
                                    base[1] = 0
                                    game.away_score += 1  # 어웨이팀 점수 + 1
                                    game.inning_away_score += 1  # 해당이닝 어웨이팀 점수 + 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1  # 홈팀 중계투수 실점 + 1
                                elif base == [0, 1, 0]:  # 주자가 2루에 있을 경우
                                    base[0] = 1  # 주자 1, 3루
                                    base[2] = 1
                                    base[1] = 0
                                elif base == [0, 0, 1]:  # 주자가 3루에 있을 경우
                                    base[0] = 1  # 주자 1루
                                    base[2] = 0
                                    game.away_score += 1  # 어웨이팀 점수, 해당이닝 점수 + 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1  # 홈팀 중계투수 실점 + 1
                                elif base == [1, 1, 1]:  # 주자 만루일 경우
                                    game.away_score += 1  # 어웨이팀 점수, 해당이닝 점수, 홈팀 투수 실점 + 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1

                                self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자,' + str(res))
                                self.record_send(str(inning) + '회 : ' + '루 '.join(base) + ',' + '원정' + game.away_score + ':' +
                                                 game.home_score + '홈')
                                if home_pitcher == home_sp:  # 투수 투구 수 추가
                                    home_sp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_sp_pitch_count))
                                if home_pitcher == home_rp:
                                    home_rp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_rp_pitch_count))
                                elif home_pitcher == home_cp:
                                    home_cp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_cp_pitch_count))
                            elif res == '2루타':  # 2루타일 경우
                                away_hitterIndex += 1
                                if away_hitterIndex == 9:
                                    away_hitterIndex = 0
                                if base == [0, 0, 0]:  # 주자 없을 경우
                                    base[1] = 1  # 주자 2루
                                elif base == [1, 0, 0]:  # 주자 1루에 있을 경우
                                    base[1] = 1  # 주자 2, 3루
                                    base[2] = 1
                                    base[0] = 0
                                elif base == [1, 1, 0]:  # 주자 1, 2루에 있을 경우
                                    base[2] = 1  # 주자 2루, 어웨이팀 점수, 해당이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    base[0] = 0
                                    game.away_score += 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1
                                elif base == [1, 0, 1]:  # 주자 1, 3루에 있을 경우
                                    base[1] = 1  # 주자 2, 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    base[0] = 0
                                    game.away_score += 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1
                                elif base == [0, 1, 1]:  # 주자 2, 3루에 있을 경우
                                    base[2] = 0  # 주자 2루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 2
                                    game.away_score += 2
                                    game.inning_away_score += 2
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 2
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 2
                                elif base == [0, 1, 0]:  # 주자 2루에 있을 경우
                                    game.away_score += 1  # 주자 2루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1
                                elif base == [0, 0, 1]:  # 주자 3루에 있을 경우
                                    base[1] = 1  # 주자 2루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    base[0] = 0
                                    game.away_score += 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1
                                elif base == [1, 1, 1]:  # 주자 만루일 경우
                                    base[0] = 0  # 주자 2, 3 루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 선발투수 실점 + 2
                                    game.away_score += 2
                                    game.inning_away_score += 2
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 2
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 2

                                self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자,' + str(res))
                                self.record_send(str(inning) + '회 : ' + "루 ".join(base) + ', ' + '원정' + str(game.away_score) +
                                                 ':' + str(game.home_score) + '홈')
                                if home_pitcher == home_sp:  # 홈팀 투수 투구 수 증가
                                    home_sp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_sp_pitch_count))
                                if home_pitcher == home_rp:
                                    home_rp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_rp_pitch_count))
                                elif home_pitcher == home_cp:
                                    home_cp_pitch_count += game.pitch_count()
                                    self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_cp_pitch_count))
                            elif res == '3루타':  # 3루타일 경우
                                away_hitter_num += 1
                                if away_hitter_num == 10:
                                    away_hitter_num = 1
                                if base == [0, 0, 0]:  # 주자 없을 경우
                                    base[2] = 1  # 주자 3루
                                elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:  # 주자 1루, 2루, 3루 일 경우
                                    base = [0, 0, 1]  # 주자 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    game.away_score += 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1
                                elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:  # 주자 1, 2루, 1, 3루, 2, 3루 일 경우
                                    base = [0, 0, 1]  # 주자 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 2
                                    game.away_score += 2
                                    game.inning_away_score += 2
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 2
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 2
                                elif base == [1, 1, 1]:  # 주자 만루일 경우
                                    base[0] = 0  # 주자 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 3
                                    base[1] = 0
                                    game.away_score += 3
                                    game.inning_away_score += 3
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 3
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 3

                                self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자,' + str(res))
                                self.record_send(str(inning) + '회 : ' + "루 ".join(base) + ', ' + '원정' + str(game.away_score) +
                                                 ':' + str(game.home_score) + '홈')
                                if home_pitcher == home_sp:
                                    home_sp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(home_sp_pitch_count))
                                if home_pitcher == home_rp:
                                    home_rp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(home_rp_pitch_count))
                                elif home_pitcher == home_cp:
                                    home_cp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(home_cp_pitch_count))
                            elif res == '홈런':  # 홈런일 경우
                                away_hitter_num += 1
                                if away_hitter_num == 10:
                                    away_hitter_num = 1
                                if base == [0, 0, 0]:  # 주자 없을 경우
                                    game.away_score += 1  # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1
                                elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:  # 주자 1명 있을 경우
                                    base = [0, 0, 0]  # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 2
                                    game.away_score += 2
                                    game.inning_away_score += 2
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 2
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 2
                                elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:  # 주자 2명 있을 경우
                                    base = [0, 0, 0]  # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 3
                                    game.away_score += 3
                                    game.inning_away_score += 3
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 3
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 3
                                elif base == [1, 1, 1]:  # 주자 만루일 경우
                                    base = [0, 0, 0]  # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 4
                                    game.away_score += 4
                                    game.inning_away_score += 4
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 4
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 4

                                self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자,' + str(res))
                                self.record_send(
                                    str(inning) + '회 : ' + "루 ".join(base) + ', ' + '원정' + str(game.away_score) +
                                    ':' + str(game.home_score) + '홈')

                                if home_pitcher == home_sp:
                                    home_sp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(home_sp_pitch_count))
                                if home_pitcher == home_rp:
                                    home_rp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(home_rp_pitch_count))
                                elif home_pitcher == home_cp:
                                    home_cp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(home_cp_pitch_count))
                            else:  # 볼넷일 경우
                                away_hitter_num += 1
                                if away_hitter_num == 10:
                                    away_hitter_num = 1
                                if base == [0, 0, 0]:  # 주자 없을 경우
                                    base[0] = 1  # 주자 1루
                                elif base == [1, 0, 0]:  # 주자 1루일 경우
                                    base[1] = 1  # 주자 1, 2 루
                                elif base == [1, 1, 0]:  # 주자 1, 2루일 경우
                                    base[2] = 1  # 주자 만루
                                elif base == [1, 0, 1]:  # 주자 1, 3루일 경우
                                    base[1] = 1  # 주자 만루
                                elif base == [0, 1, 1]:  # 주자 2, 3루일 경우
                                    base[0] = 1  # 주자 만루
                                elif base == [0, 1, 0]:  # 주자 2루일 경우
                                    base[0] = 1  # 주자 1, 2루
                                elif base == [0, 0, 1]:  # 주자 3루일 경우
                                    base[0] = 1  # 주자 1, 3루
                                elif base == [1, 1, 1]:  # 주자 만루일 경우
                                    game.away_score += 1  # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                    game.inning_away_score += 1
                                    if home_pitcher == home_sp:
                                        home_sp_scored += 1
                                    if home_pitcher == home_rp:
                                        home_rp_scored += 1

                                self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자,' + str(res))
                                self.record_send(
                                    str(inning) + '회 : ' + "루 ".join(base) + ', ' + '원정' + str(game.away_score) +
                                    ':' + str(game.home_score) + '홈')
                                if home_pitcher == home_sp:
                                    home_sp_pitch_count += game.pitch_count_case_BB()
                                    self.record_send('투구 수 : ' + str(home_sp_pitch_count))
                                if home_pitcher == home_rp:
                                    home_rp_pitch_count += game.pitch_count_case_BB()
                                    self.record_send('투구 수 : ' + str(home_rp_pitch_count))
                                elif home_pitcher == home_cp:
                                    home_cp_pitch_count += game.pitch_count_case_BB()
                                    self.record_send('투구 수 : ' + str(home_cp_pitch_count))
                            continue

                        self.record_send(str(out) + '아웃')

                    self.record_send('3 아웃 change')  # 3아웃 됐을 시, 베이스 초기화
                    self.record_send('-----------------' + str(inning) + '회 초 종료,' + '원정' +
                                     str(game.away_score) + ':' + str(game.home_score) + '홈' +
                          '------------------')

                    base = [0, 0, 0]
                    away_score_list = [inning, game.inning_away_score]
                    self.record_send('어웨이팀,' + '이닝,' + '점수' + str(away_score_list))
                    game.inning_away_score = 0
                    if inning > 8 and game.home_score > game.away_score:  # 9회 이상일때, 홈팀 점수가 어웨이 보다 높으면 종료
                        break
                    else:
                        self.record_send('-----------------' + str(inning) + '회 말 홈팀 공격 -----------------')
                else:
                    out = 0
                    while True:
                        if away_sp_pitch_count > 100 or away_sp_scored > 3:
                            self.record_send('rp로 투수 교체')
                            away_sp_pitch_count = 0
                            away_sp_scored = 0
                            away_pitcher = away_rp
                        if away_pitcher == away_rp and (away_rp_pitch_count > 100 or away_rp_scored > 3):
                            self.record_send('cp로 투수 교체')
                            away_rp_pitch_count = 0
                            away_rp_scored = 0
                            away_pitcher = away_cp
                        if game.main(pitcher_league_obp, batter_league_obp):
                            o_res = game.out_result()[0]
                            out += 1
                            home_hitter_num += 1
                            if home_hitter_num == 10:
                                home_hitter_num = 1
                            print(home_hitter_num, '번 타자, ', o_res)
                            if away_pitcher == away_sp:
                                if o_res == '삼진':
                                    away_sp_pitch_count += game.pitch_count_case_K()
                                    print('투구 수 : ', away_sp_pitch_count)
                                else:
                                    away_sp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_sp_pitch_count)
                            if away_pitcher == away_rp:
                                if o_res == '삼진':
                                    away_rp_pitch_count += game.pitch_count_case_K()
                                    print('투구 수 : ', away_rp_pitch_count)
                                else:
                                    away_rp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_rp_pitch_count)
                            elif away_pitcher == away_cp:
                                if o_res == '삼진':
                                    away_cp_pitch_count += game.pitch_count_case_K()
                                    print('투구 수 : ', away_cp_pitch_count)
                                else:
                                    away_cp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_cp_pitch_count)
                            if out == 3:
                                break
                        else:
                            res = game.hit_result()[0]
                            if res == '안타':
                                home_hitter_num += 1
                                if home_hitter_num == 10:
                                    home_hitter_num = 1
                                if base == [0, 0, 0]:
                                    base[0] = 1
                                elif base == [1, 0, 0]:
                                    base[1] = 1
                                elif base == [1, 1, 0]:
                                    base[2] = 1
                                elif base == [1, 0, 1]:
                                    base[1] = 1
                                    base[2] = 0
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [0, 1, 1]:
                                    base[0] = 1
                                    base[1] = 0
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [0, 1, 0]:
                                    base[0] = 1
                                    base[2] = 1
                                    base[1] = 0
                                elif base == [0, 0, 1]:
                                    base[0] = 1
                                    base[2] = 0
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [1, 1, 1]:
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1

                                print(home_hitter_num, '번 타자,', res)
                                print(base, ',', '원정', game.away_score, ':', game.home_score, '홈')
                                if away_pitcher == away_sp:
                                    away_sp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_sp_pitch_count)
                                if away_pitcher == away_rp:
                                    away_rp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_rp_pitch_count)
                                elif away_pitcher == away_cp:
                                    away_cp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_cp_pitch_count)
                                if inning == 9 and game.home_score > game.away_score:
                                    break

                            elif res == '2루타':
                                home_hitter_num += 1
                                if home_hitter_num == 10:
                                    home_hitter_num = 1
                                if base == [0, 0, 0]:
                                    base[1] = 1
                                elif base == [1, 0, 0]:
                                    base[1] = 1
                                    base[2] = 1
                                    base[0] = 0
                                elif base == [1, 1, 0]:
                                    base[2] = 1
                                    base[0] = 0
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [1, 0, 1]:
                                    base[1] = 1
                                    base[0] = 0
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [0, 1, 1]:
                                    base[2] = 0
                                    game.home_score += 2
                                    game.inning_home_score += 2
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 2
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 2
                                elif base == [0, 1, 0]:
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [0, 0, 1]:
                                    base[1] = 1
                                    base[0] = 0
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [1, 1, 1]:
                                    base[0] = 0
                                    game.home_score += 2
                                    game.inning_home_score += 2
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 2
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 2

                                print(home_hitter_num, '번 타자,', res)
                                print(base, ',', '원정', game.away_score, ':', game.home_score, '홈')
                                if away_pitcher == away_sp:
                                    away_sp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_sp_pitch_count)
                                if away_pitcher == away_rp:
                                    away_rp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_rp_pitch_count)
                                elif away_pitcher == away_cp:
                                    away_cp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_cp_pitch_count)
                                if inning == 9 and game.home_score > game.away_score:
                                    break

                            elif res == '3루타':
                                home_hitter_num += 1
                                if home_hitter_num == 10:
                                    home_hitter_num = 1
                                if base == [0, 0, 0]:
                                    base[2] = 1
                                elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:
                                    base = [0, 0, 1]
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:
                                    base = [0, 0, 1]
                                    game.home_score += 2
                                    game.inning_home_score += 2
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 2
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 2
                                elif base == [1, 1, 1]:
                                    base[0], base[1] = 0, 0
                                    game.home_score += 3
                                    game.inning_home_score += 3
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 3
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 3

                                print(home_hitter_num, '번 타자,', res)
                                print(base, ',', '원정', game.away_score, ':', game.home_score, '홈')
                                if away_pitcher == away_sp:
                                    away_sp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_sp_pitch_count)
                                if away_pitcher == away_rp:
                                    away_rp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_rp_pitch_count)
                                elif away_pitcher == away_cp:
                                    away_cp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_cp_pitch_count)
                                if inning == 9 and game.home_score > game.away_score:
                                    break

                            elif res == '홈런':
                                home_hitter_num += 1
                                if home_hitter_num == 10:
                                    home_hitter_num = 1
                                if base == [0, 0, 0]:
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1
                                elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:
                                    base = [0, 0, 0]
                                    game.home_score += 2
                                    game.inning_home_score += 2
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 2
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 2
                                elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:
                                    base = [0, 0, 0]
                                    game.home_score += 3
                                    game.inning_home_score += 3
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 3
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 3
                                elif base == [1, 1, 1]:
                                    base = [0, 0, 0]
                                    game.home_score += 4
                                    game.inning_home_score += 4
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 4
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 4

                                print(home_hitter_num, '번 타자,', res)
                                print('원정', game.away_score, ':', game.home_score, '홈')
                                if away_pitcher == away_sp:
                                    away_sp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_sp_pitch_count)
                                if away_pitcher == away_rp:
                                    away_rp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_rp_pitch_count)
                                elif away_pitcher == away_cp:
                                    away_cp_pitch_count += game.pitch_count()
                                    print('투구 수 : ', away_cp_pitch_count)
                                if inning == 9 and game.home_score > game.away_score:
                                    break

                            else:
                                home_hitter_num += 1
                                if home_hitter_num == 10:
                                    home_hitter_num = 1
                                if base == [0, 0, 0]:
                                    base[0] = 1
                                elif base == [1, 0, 0]:
                                    base[1] = 1
                                elif base == [1, 1, 0]:
                                    base[2] = 1
                                elif base == [1, 0, 1]:
                                    base[1] = 1
                                elif base == [0, 1, 1]:
                                    base[0] = 1
                                elif base == [0, 1, 0]:
                                    base[0] = 1
                                elif base == [0, 0, 1]:
                                    base[0] = 1
                                elif base == [1, 1, 1]:
                                    game.home_score += 1
                                    game.inning_home_score += 1
                                    if away_pitcher == away_sp:
                                        away_sp_scored += 1
                                    if away_pitcher == away_rp:
                                        away_rp_scored += 1

                                print(home_hitter_num, '번 타자,', res)
                                print(base, ',', '원정', game.away_score, ':', game.home_score, '홈')
                                if away_pitcher == away_sp:
                                    away_sp_pitch_count += game.pitch_count_case_BB()
                                    print('투구 수 : ', away_sp_pitch_count)
                                if away_pitcher == away_rp:
                                    away_rp_pitch_count += game.pitch_count_case_BB()
                                    print('투구 수 : ', away_rp_pitch_count)
                                elif away_pitcher == away_cp:
                                    away_cp_pitch_count += game.pitch_count_case_BB()
                                    print('투구 수 : ', away_cp_pitch_count)

                            continue

                        if inning > 8 and game.home_score > game.away_score:
                            break
                        print(out, '아웃')

                    print('3 아웃 change')
                    print('-----------------', inning, '회 말 종료,', '원정', game.away_score, ':', home_score, '홈',
                          '------------------')
                    base = [0, 0, 0]
                    home_score_list = [inning, game.inning_home_score]
                    print('홈팀,', '이닝,', '점수', home_score_list)
                    game.inning_home_score = 0

            if inning > 8 and (game.home_score > game.away_score or
                               game.home_score < game.away_score):
                break

            else:
                continue

        print('경기 종료')
        if game.home_score > game.away_score:
            print('홈팀 승리')
        elif game.away_score > game.home_score:
            print('원정팀 승리')
        else:
            print('무승부')
