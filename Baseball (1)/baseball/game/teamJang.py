from random import choices
from bs4 import BeautifulSoup

#def home_team_line_up():


#def away_team_line_up():


def batter():
    fp = open("STATIZ_batter.html", encoding='utf-8')

    soup = BeautifulSoup(fp, "html.parser")

    batter_name = soup.select('a')[96].string
    return batter_name

def pitcher():
    fp = open("STATIZ_pitcher.html", encoding='utf-8')

    soup = BeautifulSoup(fp, "html.parser")

    pitcher_name = soup.select('a')[95].string
    return pitcher_name

def batter_OBP():       # 타자 출루율
    fp = open("STATIZ_batter.html", encoding="utf-8")

    soup = BeautifulSoup(fp, "html.parser")

    batter_obp = float('0' + soup.select("span")[225].string)
    #print(batter(), '의 출루율 : ', batter_obp)
    return batter_obp

def pitcher_OBP():      # 투수 피출루율
    fp = open("STATIZ_pitcher.html", encoding="utf-8")

    soup = BeautifulSoup(fp, "html.parser")

    pitcher_obp = float('0' + soup.select("span")[165].string)
    #print(pitcher(), '의 피출루율 : ', pitcher_obp)
    return pitcher_obp

def pitcher_league_OBP():       # 투수리그 피출루율
    pitcher_year = 0
    pitcher_year_obp = 0.353
    return pitcher_year_obp

def batter_league_OBP():        # 타자리그 출루율
    batter_year = 0
    batter_year_obp = 0.357
    return batter_year_obp

def hit_result():       # 안타 결과(안타, 2루타, 3루타, 홈런, 볼넷 출력)
    fp = open("STATIZ_batter.html", encoding="utf-8")

    soup = BeautifulSoup(fp, "html.parser")

    hit = int(soup.select('span')[209].string) + int(soup.select('span')[217].string)
    BB = int(soup.select("span")[217].string)
    hit_one = int(soup.select('span')[209].string) - int(soup.select('span')[210].string) - int(
        soup.select('span')[211].string) - int(soup.select('span')[212].string)
    hit_two = int(soup.select('span')[210].string)
    hit_three = int(soup.select('span')[211].string)
    homerun = int(soup.select('span')[212].string)

    hit_kind = ['안타', '2루타', '3루타', '홈런', '볼넷']
    run_rate = [hit_one / hit, hit_two / hit, hit_three / hit, homerun / hit, BB / hit]

    hit_def = choices(hit_kind, run_rate)
    #print('출루 성공! : ' + hit_def[0])
    return hit_def

def out_result():       # 아웃 결과 (삼진, 뜬공, 땅볼 중 출력)
    fp1 = open("STATIZ_pitcher_basic.html", encoding="utf-8")
    fp2 = open("STATIZ_pitcher_2.html", encoding='utf-8')

    soup = BeautifulSoup(fp1, "html.parser")
    soup2 = BeautifulSoup(fp2, "html.parser")

    inning = float(soup.select('span')[181].string)
    #print(inning)
    out_count = int((soup.select('span')[181].string).split('.')[0]) * 3 + int(
        (soup.select('span')[181].string).split('.')[1])
    #print(out_count)
    strike_out = int(soup.select('span')[192].string)
    #print(strike_out)
    flyball_out = int(soup2.select('span')[785].string)
    #print(flyball_out)
    groundball_out = int(soup2.select('span')[786].string)
    #print(groundball_out)

    out_kind = ['삼진', '땅볼아웃', '뜬공아웃']
    #out_rate = [strike_out / out_count, flyball_out / out_count, groundball_out / out_count]
    out_rate = [0.3333333334, 0.3333333333, 0.3333333333]
    # 특정 년도 이전에는 땅볼, 뜬공 기록이 없기에 각각 1/3 확률로 나오도록 설정

    out_def = choices(out_kind, out_rate)
    #print('아웃! : ' + out_def[0])
    return out_def

def main():     # 타자 투수 대결 결과 (안타, 아웃 중 출력)
    pitcher = pitcher_OBP()
    batter = batter_OBP()
    batter_oz = batter / (1 - batter)
    pitcher_oz = (1 - pitcher) / pitcher
    pitcher_league_obp = pitcher_league_OBP()
    batter_league_obp = batter_league_OBP()
    pitcher_league_obp_oz = (1 - pitcher_league_obp) / pitcher_league_obp
    batter_league_obp_oz = batter_league_obp / (1 - batter_league_obp)
    total_league_OBP_avg = 0.340
    total_league_OBP_avg_oz = total_league_OBP_avg / (1 - total_league_OBP_avg)
    OR = ((batter_oz / batter_league_obp_oz) / (pitcher_oz / pitcher_league_obp_oz)) * total_league_OBP_avg_oz
    result = round(OR / (1 + OR), 3)

    #print('타자가 투수를 상대로 출루를 할 확률 : ', result)

    hit_or_out = ['안타', '아웃']
    hit_rate = [result, 1 - result]

    total_result = choices(hit_or_out, hit_rate)

    if total_result[0] == '안타':
        return False
    else:
        return True

def pitch_count():      # 투구 수 결과 (투구 수 1 ~ 10개 중 출력)
    pitch_count_kind = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    hit_count_rate = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.07, 0.07, 0.07, 0.07]
    pitch_count_def = choices(pitch_count_kind, hit_count_rate)
    pitch_count = int(pitch_count_def[0])
    return pitch_count

def pitch_count_case_BB():       # 볼넷일 시 투구수 결과 (투구 수 3 ~ 10개 중 출력)

    pitch_count_kind = [4, 5, 6, 7, 8, 9, 10]
    hit_count_rate = [0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]
    pitch_count_def = choices(pitch_count_kind, hit_count_rate)
    pitch_count = int(pitch_count_def[0])
    return pitch_count

def pitch_count_case_K():       # 삼진일 시 투구수 결과 (투구 수 3 ~ 10개 중 출력)

    pitch_count_kind = [3, 4, 5, 6, 7, 8, 9, 10]
    hit_count_rate = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
    pitch_count_def = choices(pitch_count_kind, hit_count_rate)
    pitch_count = int(pitch_count_def[0])
    return pitch_count

def inning_proc():      # 경기 진행 로직
    home_score = 0      # 홈팀 점수
    away_score = 0      # 어웨이팀 점수
    inning_home_score = 0       # 이닝당 홈팀 점수
    inning_away_score = 0       # 이닝당 어웨이팀 점수
    home_hitter_num = 0     # 홈팀 타자 번호
    away_hitter_num = 0     # 어웨이팀 타자 번호
    innings = range(1, 13)      # 이닝(1 ~ 12)
    base = [0, 0, 0]        # 베이스 리스트, [0] = 1루, [1] = 2루, [2] = 3루

    away_pitcher_num = [0, 1, 2]        # 어웨이팀 투수 번호(선발:1, 중계:2, 마무리:3)
    away_sp = away_pitcher_num[0]       # 어웨이팀 선발투수
    away_rp = away_pitcher_num[1]       # 어웨이팀 중계투수
    away_cp = away_pitcher_num[2]       # 어웨이팀 마무리투수
    away_sp_pitch_count = 0         # 어웨이팀 선발투수 투구 수
    away_rp_pitch_count = 0         # 어웨이팀 중계투수 투구 수
    away_cp_pitch_count = 0         # 어웨이팀 마무리투수 투구 수
    away_sp_scored = 0          # 어웨이팀 선발투수 실점
    away_rp_scored = 0          # 어웨이팀 중계투수 실점
    away_pitcher = away_sp      # 어웨이팀 투수 초기설정은 선발투수

    home_pitcher_num = [0, 1, 2]        # 홈팀 투수 번호(선발:1, 중계:2, 마무리:3)
    home_sp = home_pitcher_num[0]        # 홈팀 선발투수
    home_rp = home_pitcher_num[1]        # 홈팀 중계투수
    home_cp = home_pitcher_num[2]        # 홈팀 마무리투수
    home_sp_pitch_count = 0        # 홈팀 선발투수 투구 수
    home_rp_pitch_count = 0        # 홈팀 중계투수 투구 수
    home_cp_pitch_count = 0        # 홈팀 마무리투수 투구 수
    home_sp_scored = 0        # 홈팀 선발투수 실점
    home_rp_scored = 0        # 홈팀 중계투수 실점
    home_pitcher = home_sp        # 홈팀 투수 초기설정은 선발투수

    for inning in innings:      # 9 ~ 12이닝
        for top_and_bottom in range(1, 3):      # 이닝별 초, 말
            if top_and_bottom == 1:     # 이닝 초
                out = 0
                print('-----------------', inning, '회 초 원정팀 공격 -----------------')
                while True:         # 3아웃 되는 동안 실행
                    if home_sp_pitch_count > 100 or home_sp_scored > 3:     # 선발투수 투구 수가 100개 초과이거나 3실점 초과일 경우
                        print('rp로 투수 교체')
                        home_sp_pitch_count = 0
                        home_sp_scored = 0
                        home_pitcher = home_rp
                    if home_pitcher == home_rp and (home_rp_pitch_count > 100 or home_rp_scored > 3):       # 중계투수 투구 수가 100개 초과이거나 3실점 초과일 경우
                        print('cp로 투수 교체')
                        home_rp_pitch_count = 0
                        home_rp_scored = 0
                        home_pitcher = home_cp
                    if main():      # 투수 VS 타자가 아웃일 경우
                        o_res = out_result()[0]
                        out += 1        # 아웃카운트 추가
                        away_hitter_num += 1        # 다음타자
                        if away_hitter_num == 10:       # 9번 타자 다음은 1번 타자
                            away_hitter_num = 1
                        print(away_hitter_num, '번 타자, ', o_res)
                        if home_pitcher == home_sp:     # 투수가 선발투수일 시 투구 수 추가
                            if o_res == '삼진':
                                home_sp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', home_sp_pitch_count)
                            else:
                                home_sp_pitch_count += pitch_count()
                                print('투구 수 : ', home_sp_pitch_count)
                        if home_pitcher == home_rp:     # 투수가 중계투수일 시 투구 수 추가
                            if o_res == '삼진':
                                home_rp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', home_rp_pitch_count)
                            else:
                                home_rp_pitch_count += pitch_count()
                                print('투구 수 : ', home_rp_pitch_count)
                        if home_pitcher == home_cp:     # 투수가 마무리투수일 시 투구 수 추가
                            if o_res == '삼진':
                                home_cp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', home_cp_pitch_count)
                            else:
                                home_cp_pitch_count += pitch_count()
                                print('투구 수 : ', home_cp_pitch_count)
                        if out == 3:        # 3아웃일 시
                            break
                    else:           # 투수 VS 타자가 안타일 경우
                        res = hit_result()[0]
                        if res == '안타':     # 안타일 경우
                            away_hitter_num += 1        # 타자번호 + 1
                            if away_hitter_num == 10:       # 9번타자 다음은 1번타자
                                away_hitter_num = 1
                            if base == [0, 0, 0]:       # 베이스에 아무도 없을 경우
                                base[0] = 1             # 주자 1루
                            elif base == [1, 0, 0]:     # 주자가 1루에만 있을 경우
                                base[1] = 1             # 주자 1, 2루
                            elif base == [1, 1, 0]:     # 주자가 1, 2루에 있을 경우
                                base[2] = 1             # 주자 만루
                            elif base == [1, 0, 1]:     # 주자가 1, 3루에 있을 경우
                                base[1] = 1             # 주자 1, 2루
                                base[2] = 0
                                away_score += 1         # 어웨이팀 점수 + 1
                                inning_away_score += 1  # 해당이닝 어웨이팀 점수 + 1
                                if home_pitcher == home_sp:     # 홈팀 투수 선발투수일 경우
                                    home_sp_scored += 1         # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:     # 홈팀 투수 중계투수일 경우
                                    home_rp_scored += 1         # 홈팀 중계투수 실점 + 1
                            elif base == [0, 1, 1]:     # 주자가 2, 3루에 있을 경우
                                base[0] = 1             # 주자 1, 3루
                                base[1] = 0
                                away_score += 1         # 어웨이팀 점수 + 1
                                inning_away_score += 1  # 해당이닝 어웨이팀 점수 + 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1     # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1     # 홈팀 중계투수 실점 + 1
                            elif base == [0, 1, 0]:     # 주자가 2루에 있을 경우
                                base[0] = 1             # 주자 1, 3루
                                base[2] = 1
                                base[1] = 0
                            elif base == [0, 0, 1]:     # 주자가 3루에 있을 경우
                                base[0] = 1             # 주자 1루
                                base[2] = 0
                                away_score += 1         # 어웨이팀 점수, 해당이닝 점수 + 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1     # 홈팀 선발투수 실점 + 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1     # 홈팀 중계투수 실점 + 1
                            elif base == [1, 1, 1]:     # 주자 만루일 경우
                                away_score += 1         # 어웨이팀 점수, 해당이닝 점수, 홈팀 투수 실점 + 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1

                            print(away_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if home_pitcher == home_sp:                     # 투수 투구 수 추가
                                home_sp_pitch_count += pitch_count()
                                print('투구 수 : ', home_sp_pitch_count)
                            if home_pitcher == home_rp:
                                home_rp_pitch_count += pitch_count()
                                print('투구 수 : ', home_rp_pitch_count)
                            elif home_pitcher == home_cp:
                                home_cp_pitch_count += pitch_count()
                                print('투구 수 : ', home_cp_pitch_count)
                        elif res == '2루타':          # 2루타일 경우
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:       # 주자 없을 경우
                                base[1] = 1             # 주자 2루
                            elif base == [1, 0, 0]:     # 주자 1루에 있을 경우
                                base[1] = 1             # 주자 2, 3루
                                base[2] = 1
                                base[0] = 0
                            elif base == [1, 1, 0]:     # 주자 1, 2루에 있을 경우
                                base[2] = 1             # 주자 2루, 어웨이팀 점수, 해당이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                base[0] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 0, 1]:     # 주자 1, 3루에 있을 경우
                                base[1] = 1             # 주자 2, 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                base[0] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [0, 1, 1]:     # 주자 2, 3루에 있을 경우
                                base[2] = 0             # 주자 2루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 2
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2
                            elif base == [0, 1, 0]:     # 주자 2루에 있을 경우
                                away_score += 1         # 주자 2루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [0, 0, 1]:     # 주자 3루에 있을 경우
                                base[1] = 1             # 주자 2루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                base[0] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 1, 1]:     # 주자 만루일 경우
                                base[0] = 0             # 주자 2, 3 루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 선발투수 실점 + 2
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2

                            print(away_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if home_pitcher == home_sp:                     # 홈팀 투수 투구 수 증가
                                home_sp_pitch_count += pitch_count()
                                print('투구 수 : ', home_sp_pitch_count)
                            if home_pitcher == home_rp:
                                home_rp_pitch_count += pitch_count()
                                print('투구 수 : ', home_rp_pitch_count)
                            elif home_pitcher == home_cp:
                                home_cp_pitch_count += pitch_count()
                                print('투구 수 : ', home_cp_pitch_count)
                        elif res == '3루타':              # 3루타일 경우
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:           # 주자 없을 경우
                                base[2] = 1                 # 주자 3루
                            elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:       # 주자 1루, 2루, 3루 일 경우
                                base = [0, 0, 1]        # 주자 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:       # 주자 1, 2루, 1, 3루, 2, 3루 일 경우
                                base = [0, 0, 1]        # 주자 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 2
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2
                            elif base == [1, 1, 1]:     # 주자 만루일 경우
                                base[0] = 0             # 주자 3루, 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 3
                                base[1] = 0
                                away_score += 3
                                inning_away_score += 3
                                if home_pitcher == home_sp:
                                    home_sp_scored += 3
                                if home_pitcher == home_rp:
                                    home_rp_scored += 3

                            print(away_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if home_pitcher == home_sp:
                                home_sp_pitch_count += pitch_count()
                                print('투구 수 : ', home_sp_pitch_count)
                            if home_pitcher == home_rp:
                                home_rp_pitch_count += pitch_count()
                                print('투구 수 : ', home_rp_pitch_count)
                            elif home_pitcher == home_cp:
                                home_cp_pitch_count += pitch_count()
                                print('투구 수 : ', home_cp_pitch_count)
                        elif res == '홈런':               # 홈런일 경우
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:         # 주자 없을 경우
                                away_score += 1           # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:       # 주자 1명 있을 경우
                                base = [0, 0, 0]            # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 2
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2
                            elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:       # 주자 2명 있을 경우
                                base = [0, 0, 0]        # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 3
                                away_score += 3
                                inning_away_score += 3
                                if home_pitcher == home_sp:
                                    home_sp_scored += 3
                                if home_pitcher == home_rp:
                                    home_rp_scored += 3
                            elif base == [1, 1, 1]:         # 주자 만루일 경우
                                base = [0, 0, 0]        # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 4
                                away_score += 4
                                inning_away_score += 4
                                if home_pitcher == home_sp:
                                    home_sp_scored += 4
                                if home_pitcher == home_rp:
                                    home_rp_scored += 4

                            print(away_hitter_num, '번 타자,', res)
                            print('원정', away_score, ':', home_score, '홈')
                            if home_pitcher == home_sp:
                                home_sp_pitch_count += pitch_count()
                                print('투구 수 : ', home_sp_pitch_count)
                            if home_pitcher == home_rp:
                                home_rp_pitch_count += pitch_count()
                                print('투구 수 : ', home_rp_pitch_count)
                            elif home_pitcher == home_cp:
                                home_cp_pitch_count += pitch_count()
                                print('투구 수 : ', home_cp_pitch_count)
                        else:           # 볼넷일 경우
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:       # 주자 없을 경우
                                base[0] = 1             # 주자 1루
                            elif base == [1, 0, 0]:     # 주자 1루일 경우
                                base[1] = 1             # 주자 1, 2 루
                            elif base == [1, 1, 0]:     # 주자 1, 2루일 경우
                                base[2] = 1             # 주자 만루
                            elif base == [1, 0, 1]:     # 주자 1, 3루일 경우
                                base[1] = 1             # 주자 만루
                            elif base == [0, 1, 1]:     # 주자 2, 3루일 경우
                                base[0] = 1             # 주자 만루
                            elif base == [0, 1, 0]:     # 주자 2루일 경우
                                base[0] = 1             # 주자 1, 2루
                            elif base == [0, 0, 1]:     # 주자 3루일 경우
                                base[0] = 1             # 주자 1, 3루
                            elif base == [1, 1, 1]:     # 주자 만루일 경우
                                away_score += 1         # 어웨이 점수, 이닝 어웨이 점수, 홈팀 투수 실점 + 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1

                            print(away_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if home_pitcher == home_sp:
                                home_sp_pitch_count += pitch_count_case_BB()
                                print('투구 수 : ', home_sp_pitch_count)
                            if home_pitcher == home_rp:
                                home_rp_pitch_count += pitch_count_case_BB()
                                print('투구 수 : ', home_rp_pitch_count)
                            elif home_pitcher == home_cp:
                                home_cp_pitch_count += pitch_count_case_BB()
                                print('투구 수 : ', home_cp_pitch_count)
                        continue

                    print(out, '아웃')

                print('3 아웃 change')        # 3아웃 됐을 시, 베이스 초기화
                print('-----------------', inning, '회 초 종료,', '원정', away_score, ':', home_score, '홈', '------------------')
                base = [0, 0, 0]
                away_score_list = [inning, inning_away_score]
                print('어웨이팀,', '이닝,', '점수', away_score_list)
                inning_away_score = 0
                if inning > 8 and home_score > away_score:     # 9회 이상일때, 홈팀 점수가 어웨이 보다 높으면 종료
                    break
                else:
                    print('-----------------', inning, '회 말 홈팀 공격 -----------------')
            else:
                out = 0
                while True:
                    if away_sp_pitch_count > 100 or away_sp_scored > 3:
                        print('rp로 투수 교체')
                        away_sp_pitch_count = 0
                        away_sp_scored = 0
                        away_pitcher = away_rp
                    if away_pitcher == away_rp and (away_rp_pitch_count > 100 or away_rp_scored > 3):
                        print('cp로 투수 교체')
                        away_rp_pitch_count = 0
                        away_rp_scored = 0
                        away_pitcher = away_cp
                    if main():
                        o_res = out_result()[0]
                        out += 1
                        home_hitter_num += 1
                        if home_hitter_num == 10:
                            home_hitter_num = 1
                        print(home_hitter_num, '번 타자, ', o_res)
                        if away_pitcher == away_sp:
                            if o_res == '삼진':
                                away_sp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', away_sp_pitch_count)
                            else:
                                away_sp_pitch_count += pitch_count()
                                print('투구 수 : ', away_sp_pitch_count)
                        if away_pitcher == away_rp:
                            if o_res == '삼진':
                                away_rp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', away_rp_pitch_count)
                            else:
                                away_rp_pitch_count += pitch_count()
                                print('투구 수 : ', away_rp_pitch_count)
                        elif away_pitcher == away_cp:
                            if o_res == '삼진':
                                away_cp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', away_cp_pitch_count)
                            else:
                                away_cp_pitch_count += pitch_count()
                                print('투구 수 : ', away_cp_pitch_count)
                        if out == 3:
                            break
                    else:
                        res = hit_result()[0]
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
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [0, 1, 1]:
                                base[0] = 1
                                base[1] = 0
                                home_score += 1
                                inning_home_score += 1
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
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [1, 1, 1]:
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1

                            print(home_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if away_pitcher == away_sp:
                                away_sp_pitch_count += pitch_count()
                                print('투구 수 : ', away_sp_pitch_count)
                            if away_pitcher == away_rp:
                                away_rp_pitch_count += pitch_count()
                                print('투구 수 : ', away_rp_pitch_count)
                            elif away_pitcher == away_cp:
                                away_cp_pitch_count += pitch_count()
                                print('투구 수 : ', away_cp_pitch_count)
                            if inning == 9 and home_score > away_score:
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
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [1, 0, 1]:
                                base[1] = 1
                                base[0] = 0
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [0, 1, 1]:
                                base[2] = 0
                                home_score += 2
                                inning_home_score += 2
                                if away_pitcher == away_sp:
                                    away_sp_scored += 2
                                if away_pitcher == away_rp:
                                    away_rp_scored += 2
                            elif base == [0, 1, 0]:
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [0, 0, 1]:
                                base[1] = 1
                                base[0] = 0
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [1, 1, 1]:
                                base[0] = 0
                                home_score += 2
                                inning_home_score += 2
                                if away_pitcher == away_sp:
                                    away_sp_scored += 2
                                if away_pitcher == away_rp:
                                    away_rp_scored += 2

                            print(home_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if away_pitcher == away_sp:
                                away_sp_pitch_count += pitch_count()
                                print('투구 수 : ', away_sp_pitch_count)
                            if away_pitcher == away_rp:
                                away_rp_pitch_count += pitch_count()
                                print('투구 수 : ', away_rp_pitch_count)
                            elif away_pitcher == away_cp:
                                away_cp_pitch_count += pitch_count()
                                print('투구 수 : ', away_cp_pitch_count)
                            if inning == 9 and home_score > away_score:
                                break

                        elif res == '3루타':
                            home_hitter_num += 1
                            if home_hitter_num == 10:
                                home_hitter_num = 1
                            if base == [0, 0, 0]:
                                base[2] = 1
                            elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:
                                base = [0, 0, 1]
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:
                                base = [0, 0, 1]
                                home_score += 2
                                inning_home_score += 2
                                if away_pitcher == away_sp:
                                    away_sp_scored += 2
                                if away_pitcher == away_rp:
                                    away_rp_scored += 2
                            elif base == [1, 1, 1]:
                                base[0], base[1] = 0
                                home_score += 3
                                inning_home_score += 3
                                if away_pitcher == away_sp:
                                    away_sp_scored += 3
                                if away_pitcher == away_rp:
                                    away_rp_scored += 3

                            print(home_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if away_pitcher == away_sp:
                                away_sp_pitch_count += pitch_count()
                                print('투구 수 : ', away_sp_pitch_count)
                            if away_pitcher == away_rp:
                                away_rp_pitch_count += pitch_count()
                                print('투구 수 : ', away_rp_pitch_count)
                            elif away_pitcher == away_cp:
                                away_cp_pitch_count += pitch_count()
                                print('투구 수 : ', away_cp_pitch_count)
                            if inning == 9 and home_score > away_score:
                                break

                        elif res == '홈런':
                            home_hitter_num += 1
                            if home_hitter_num == 10:
                                home_hitter_num = 1
                            if base == [0, 0, 0]:
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1
                            elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:
                                base = [0, 0, 0]
                                home_score += 2
                                inning_home_score += 2
                                if away_pitcher == away_sp:
                                    away_sp_scored += 2
                                if away_pitcher == away_rp:
                                    away_rp_scored += 2
                            elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:
                                base = [0, 0, 0]
                                home_score += 3
                                inning_home_score += 3
                                if away_pitcher == away_sp:
                                    away_sp_scored += 3
                                if away_pitcher == away_rp:
                                    away_rp_scored += 3
                            elif base == [1, 1, 1]:
                                base = [0, 0, 0]
                                home_score += 4
                                inning_home_score += 4
                                if away_pitcher == away_sp:
                                    away_sp_scored += 4
                                if away_pitcher == away_rp:
                                    away_rp_scored += 4

                            print(home_hitter_num, '번 타자,', res)
                            print('원정', away_score, ':', home_score, '홈')
                            if away_pitcher == away_sp:
                                away_sp_pitch_count += pitch_count()
                                print('투구 수 : ', away_sp_pitch_count)
                            if away_pitcher == away_rp:
                                away_rp_pitch_count += pitch_count()
                                print('투구 수 : ', away_rp_pitch_count)
                            elif away_pitcher == away_cp:
                                away_cp_pitch_count += pitch_count()
                                print('투구 수 : ', away_cp_pitch_count)
                            if inning == 9 and home_score > away_score:
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
                                home_score += 1
                                inning_home_score += 1
                                if away_pitcher == away_sp:
                                    away_sp_scored += 1
                                if away_pitcher == away_rp:
                                    away_rp_scored += 1

                            print(home_hitter_num, '번 타자,', res)
                            print(base, ',', '원정', away_score, ':', home_score, '홈')
                            if away_pitcher == away_sp:
                                away_sp_pitch_count += pitch_count_case_BB()
                                print('투구 수 : ', away_sp_pitch_count)
                            if away_pitcher == away_rp:
                                away_rp_pitch_count += pitch_count_case_BB()
                                print('투구 수 : ', away_rp_pitch_count)
                            elif away_pitcher == away_cp:
                                away_cp_pitch_count += pitch_count_case_BB()
                                print('투구 수 : ', away_cp_pitch_count)

                        continue

                    if inning > 8 and home_score > away_score:
                        break
                    print(out, '아웃')

                print('3 아웃 change')
                print('-----------------', inning, '회 말 종료,', '원정', away_score, ':', home_score, '홈', '------------------')
                base = [0, 0, 0]
                home_score_list = [inning, inning_home_score]
                print('홈팀,', '이닝,', '점수', home_score_list)
                inning_home_score = 0
        if inning > 8 and (home_score > away_score or home_score < away_score):
            break

        else:
            continue

    print('경기 종료')
    if home_score > away_score:
        print('홈팀 승리')
    elif away_score > home_score:
        print('원정팀 승리')
    else:
        print('무승부')

if __name__ == "__main__":
    inning_proc()