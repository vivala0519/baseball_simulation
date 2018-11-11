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

        # print("====================================================================")
        # print(message)
        # print("====================================================================")

        process = DBprocess()
        process.getBattersAndPitchers(message)

        home_batters = process.getBatterStat(process.home_batters)
        home_pitchers = process.getPitchersStat(process.home_pitchers)

        away_batters = process.getBatterStat(process.away_batters)
        away_pitchers = process.getPitchersStat(process.away_pitchers)

        # print("home_pitchers = ", home_pitchers)
        # print("=============================================================")
        # print("home_batters = ", home_batters)
        # print("=============================================================")
        # print("away_pitchers = ", away_pitchers)
        # print("=============================================================")
        # print("away_batters = ", away_batters)

        self.inning_proc(home_pitchers, home_batters, away_pitchers, away_batters)


        # self.send(text_data=json.dumps({
        #     'message': message,
        #
        # }))



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
        home_rp = homePitcherList[1] # 홈팀 중계투수
        home_cp = homePitcherList[2] # 홈팀 마무리투수
        home_sp_pitch_count = 0  # 홈팀 선발투수 투구 수
        home_rp_pitch_count = 0  # 홈팀 중계투수 투구 수
        home_cp_pitch_count = 0  # 홈팀 마무리투수 투구 수
        home_sp_scored = 0  # 홈팀 선발투수 실점
        home_rp_scored = 0  # 홈팀 중계투수 실점
        home_pitcher = home_sp  # 홈팀 투수 초기설정은 선발투수

        # print("======================================= obpBook ========================================")
        # print(obpBook)
        # print("======================================= awayPitcherList ========================================")
        # print(awayPitcherList)
        # print("======================================= homePitcherList ========================================")
        # print(homePitcherList)
        # print("======================================= awayBatterList ========================================")
        # print(awayBatterList)
        # print("======================================= homeBatterList ========================================")
        # print(homeBatterList)
        # print("======================================= home_hitter_num ========================================")
        # print(home_hitter_num)
        # print("======================================= away_hitter_num ========================================")
        # print(away_hitter_num)
        # print("======================================= away_sp ========================================")
        # print(away_sp)
        # print("======================================= away_rp ========================================")
        # print(away_rp)
        # print("======================================= away_cp ========================================")
        # print(away_cp)
        # print("======================================= away_pitcher ========================================")
        # print(away_pitcher)
        # print("======================================= home_sp ========================================")
        # print(home_sp)
        # print("======================================= home_rp ========================================")
        # print(home_rp)
        # print("======================================= home_cp ========================================")
        # print(home_cp)
        # print("======================================= home_pitcher ========================================")
        # print(home_pitcher)

        for inning in innings:  # 9 ~ 12이닝
            for top_and_bottom in range(1, 3):  # 이닝별 초, 말

                if top_and_bottom == 1:  # 이닝 초

                    self.record_send(str(inning) + '회 초 시작')

                    out = 0
                    self.record_send('-----------------'+ str(inning) + '회 초 원정팀 공격 -----------------')

                    game.setStats(away_hitter_num, home_pitcher)

                    while True:  # 3아웃 되는 동안 실행
                        if home_sp_pitch_count > 100 or home_sp_scored > 3:  # 선발투수 투구 수가 100개 초과이거나 3실점 초과일 경우
                            self.record_send(str(inning) + '회 : ' + 'rp로 투수 교체')
                            home_sp_pitch_count = 0
                            home_sp_scored = 0
                            home_pitcher = home_rp

                        if home_pitcher == home_rp and (    # 바로 위의 if문과 겹쳐서 교체는 무조건 두번이 동시에 일어나버린다.
                                home_rp_pitch_count > 100 or home_rp_scored > 3):  # 중계투수 투구 수가 100개 초과이거나 3실점 초과일 경우
                            self.record_send(str(inning) + '회 : ' + 'cp로 투수 교체')
                            home_rp_pitch_count = 0
                            home_rp_scored = 0
                            home_pitcher = home_cp

                        if game.main(home_pitcher[7], away_hitter_num[11]):  # 투수 VS 타자가 아웃일 경우
                            o_res = game.out_result()[0]
                            out += 1  # 아웃카운트 추가
                            away_hitterIndex += 1  # 다음타자
                            if away_hitterIndex == 9:  # 9번 타자 다음은 1번 타자
                                away_hitterIndex = 0
                            # 아래의 away_hitterIndex는 실제로는 [away_hitterIndex-1]번째를 가리킨다.
                            self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자, ' + str(o_res))
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

                            if res != '볼넷':
                                base_occupied = game.findOccupiedBase(base)
                                print("======================= base_occupied =======================")
                                print(base_occupied)
                                print("======================= base_occupied ======================")
                                base_on_base, score_on_base = game.countingScoreWithoutBB(base_occupied, res, game.away_score)
                                game.inning_away_score += score_on_base - game.away_score
                                print("======================= base_on_base =======================")
                                print(base_on_base)
                                print("======================= base_on_base ======================")

                                if home_pitcher == home_sp:  # 홈팀 투수 선발투수일 경우
                                    home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:  # 홈팀 투수 중계투수일 경우
                                    home_rp_scored += 1  # 홈팀 중계투수 실점 + 1


                            else:  # 볼넷일 경우
                                base_occupied = game.findOccupiedBase(base)
                                base_on_base, score_on_base = game.countingScoreOnBB(base, base_occupied, game.away_score)

                                game.inning_away_score += score_on_base - game.away_score
                                game.away_score += score_on_base - game.away_score

                                if home_pitcher == home_sp:  # 홈팀 투수 선발투수일 경우
                                    home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:  # 홈팀 투수 중계투수일 경우
                                    home_rp_scored += 1  # 홈팀 중계투수 실점 + 1


                            away_hitterIndex += 1  # 타자번호 + 1
                            if away_hitterIndex == 9:  # 9번타자 다음은 1번타자
                                away_hitterIndex = 0

                            self.record_send(str(inning) + '회 : ' + str(away_hitterIndex) + '번 타자,' + str(res))
                            self.record_send(str(inning) + '회 : ' + '루 '.join(
                                [str(base[0]), str(base[1]), str(base[2])]) +
                                             ', 원정' + str(game.away_score) + ':' + str(game.home_score) + '홈')
                            if home_pitcher == home_sp:  # 투수 투구 수 추가
                                home_sp_pitch_count += game.pitch_count()
                                self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_sp_pitch_count))
                            if home_pitcher == home_rp:
                                home_rp_pitch_count += game.pitch_count()
                                self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_rp_pitch_count))
                            elif home_pitcher == home_cp:
                                home_cp_pitch_count += game.pitch_count()
                                self.record_send(str(inning) + '회 : ' + '투구 수 : ' + str(home_cp_pitch_count))

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
                        if game.main(away_pitcher[7], home_hitter_num[11]):
                            o_res = game.out_result()[0]
                            out += 1
                            home_hitterIndex += 1
                            if home_hitterIndex == 9:
                                home_hitterIndex = 0
                            self.record_send(str(home_hitterIndex) + '번 타자, ' + o_res)
                            if away_pitcher == away_sp:
                                if o_res == '삼진':
                                    away_sp_pitch_count += game.pitch_count_case_K()
                                    self.record_send('투구 수 : ' + str(away_sp_pitch_count))
                                else:
                                    away_sp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(away_sp_pitch_count))
                            if away_pitcher == away_rp:
                                if o_res == '삼진':
                                    away_rp_pitch_count += game.pitch_count_case_K()
                                    self.record_send('투구 수 : ' + str(away_rp_pitch_count))
                                else:
                                    away_rp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(away_rp_pitch_count))
                            elif away_pitcher == away_cp:
                                if o_res == '삼진':
                                    away_cp_pitch_count += game.pitch_count_case_K()
                                    self.record_send('투구 수 : ' + str(away_cp_pitch_count))
                                else:
                                    away_cp_pitch_count += game.pitch_count()
                                    self.record_send('투구 수 : ' + str(away_cp_pitch_count))
                            if out == 3:
                                break
                        else:
                            res = game.hit_result()[0]
                            # 출루하니까 타자가 바뀐다.
                            home_hitterIndex += 1
                            if home_hitterIndex == 9:
                                home_hitterIndex = 0

                            if res != '볼넷':

                                base_occupied = game.findOccupiedBase(base)
                                base_on_base, score_on_base = game.countingScoreWithoutBB(base_occupied, res,
                                                                                          game.home_score)
                                game.inning_home_score += score_on_base - game.home_score
                                game.home_score += score_on_base - game.home_score

                                if home_pitcher == home_sp:  # 홈팀 투수 선발투수일 경우
                                    home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:  # 홈팀 투수 중계투수일 경우
                                    home_rp_scored += 1  # 홈팀 중계투수 실점 + 1

                            else:

                                base_occupied = game.findOccupiedBase(base)
                                base_on_base, score_on_base = game.countingScoreOnBB(base, base_occupied,
                                                                                     game.home_score)
                                game.inning_home_score += score_on_base - game.home_score

                                if home_pitcher == home_sp:  # 홈팀 투수 선발투수일 경우
                                    home_sp_scored += 1  # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:  # 홈팀 투수 중계투수일 경우
                                    home_rp_scored += 1  # 홈팀 중계투수 실점 + 1

                            self.record_send(str(home_hitterIndex) + '번 타자 ' + res)
                            self.record_send('원정 ' + str(game.away_score) + ' : ' + str(game.home_score) + '홈')
                            if away_pitcher == away_sp:
                                away_sp_pitch_count += game.pitch_count_case_BB()
                                self.record_send('투구 수 : ' + str(away_sp_pitch_count))
                            if away_pitcher == away_rp:
                                away_rp_pitch_count += game.pitch_count_case_BB()
                                self.record_send('투구 수 : ' + str(away_rp_pitch_count))
                            elif away_pitcher == away_cp:
                                away_cp_pitch_count += game.pitch_count_case_BB()
                                self.record_send('투구 수 : ' + str(away_cp_pitch_count))

                            continue


                        if inning > 8 and game.home_score > game.away_score:
                            break
                        self.record_send(str(out) +  '아웃')

                    self.record_send('3 아웃 change')
                    self.record_send('-----------------' + str(inning) + '회 말 종료,' + '원정 ' + str(game.away_score)
                                     + ' : ' + str(game.home_score) + ' 홈------------------')
                    base = [0, 0, 0]
                    home_score_list = [inning, game.inning_home_score]
                    self.record_send('홈팀의 ' + '이닝 // ' + '점수 : ' + str(home_score_list[0]) +
                                     " // " + str(home_score_list[1]))
                    game.inning_home_score = 0

            if inning > 8 and (game.home_score > game.away_score or
                               game.home_score < game.away_score):
                break

            else:
                continue

        self.record_send('경기 종료')
        if game.home_score > game.away_score:
            self.record_send('홈팀 승리')
        elif game.away_score > game.home_score:
            self.record_send('원정팀 승리')
        else:
            self.record_send('무승부')
