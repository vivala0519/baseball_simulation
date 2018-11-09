from random import choices
# from bs4 import BeautifulSoup


def out_count():
    out_count = 0
    out_count += 1
    print(out_count)

#def league_OBP():
    #fp = open("2018_KBO_RECORD.html", encoding="utf-8")

    #soup = BeautifulSoup(fp, "html.parser")

    #league_obp = float(soup.select("td")[148].string)
    #print('리그 평균 출루율 : ', league_obp)
    #return league_obp

def batter():
    # fp = open("STATIZ_batter.html", encoding='utf-8')
    #
    # soup = BeautifulSoup(fp, "html.parser")

    #batter_name = soup.select('a')[96].string
    batter_name = '로맥'
    return batter_name

def pitcher():
    # fp = open("STATIZ_pitcher.html", encoding='utf-8')
    #
    # soup = BeautifulSoup(fp, "html.parser")

    #pitcher_name = soup.select('a')[95].string
    pitcher_name = '김광현'
    return pitcher_name

def batter_OBP():       # 타자 출루율
    # fp = open("STATIZ_batter.html", encoding="utf-8")
    #
    # soup = BeautifulSoup(fp, "html.parser")

    #batter_obp = float('0' + soup.select("span")[225].string)
    batter_obp = 0.365
    #print(batter(), '의 출루율 : ', batter_obp)
    return batter_obp

def pitcher_OBP():      # 투수 피출루율
    # fp = open("STATIZ_pitcher.html", encoding="utf-8")
    #
    # soup = BeautifulSoup(fp, "html.parser")

    #pitcher_obp = float('0' + soup.select("span")[165].string)
    pitcher_obp = 0.344
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
    # fp = open("STATIZ_batter.html", encoding="utf-8")
    #
    # soup = BeautifulSoup(fp, "html.parser")

    # hit = int(soup.select('span')[209].string) + int(soup.select('span')[217].string)
    hit = 167
    # BB = int(soup.select("span")[217].string)
    BB = 72
    # hit_one = int(soup.select('span')[209].string) - int(soup.select('span')[210].string) - int(
    #     soup.select('span')[211].string) - int(soup.select('span')[212].string)
    hit_one = 105
    # hit_two = int(soup.select('span')[210].string)
    hit_two = 19
    # hit_three = int(soup.select('span')[211].string)
    hit_three = 0
    # homerun = int(soup.select('span')[212].string)
    homerun = 43

    hit_kind = ['안타', '2루타', '3루타', '홈런', '볼넷']
    run_rate = [hit_one / hit, hit_two / hit, hit_three / hit, homerun / hit, BB / hit]

    #hit_def = choices(hit_kind, run_rate)
    hit_def = choices(hit_kind, run_rate)
    #print('출루 성공! : ' + hit_def[0])
    return hit_def

def out_result():       # 아웃 결과 (삼진, 뜬공, 땅볼 중 출력)
    # fp1 = open("STATIZ_pitcher_basic.html", encoding="utf-8")
    # fp2 = open("STATIZ_pitcher_2.html", encoding='utf-8')
    #
    # soup = BeautifulSoup(fp1, "html.parser")
    # soup2 = BeautifulSoup(fp2, "html.parser")

    # inning = float(soup.select('span')[181].string)
    #print(inning)
    # out_count = int((soup.select('span')[181].string).split('.')[0]) * 3 + int(
    #     (soup.select('span')[181].string).split('.')[1])
    #print(out_count)
    # strike_out = int(soup.select('span')[192].string)
    #print(strike_out)
    # flyball_out = int(soup2.select('span')[785].string)
    #print(flyball_out)
    # groundball_out = int(soup2.select('span')[786].string)
    #print(groundball_out)

    out_kind = ['삼진', '땅볼아웃', '뜬공아웃']
    #out_rate = [strike_out / out_count, flyball_out / out_count, groundball_out / out_count]
    out_rate = [0.334, 0.333, 0.333]
    # 특정 년도 이전에는 땅볼, 뜬공 기록이 없기에 각각 33% 확률로 나오도록 설정

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
    home_score = 0
    away_score = 0
    inning_home_score = 0
    inning_away_score = 0
    away_hitter_num = 0
    home_hitter_num = 0
    innings = range(1, 13)
    base = [0, 0, 0]

    away_pitcher_num = [0, 1, 2]
    away_sp = away_pitcher_num[0]
    away_rp = away_pitcher_num[1]
    away_cp = away_pitcher_num[2]
    away_sp_pitch_count = 0
    away_rp_pitch_count = 0
    away_cp_pitch_count = 0
    away_sp_scored = 0
    away_rp_scored = 0
    away_pitcher = away_sp

    home_pitcher_num = [0, 1, 2]
    home_sp = home_pitcher_num[0]
    home_rp = home_pitcher_num[1]
    home_cp = home_pitcher_num[2]
    home_sp_pitch_count = 0
    home_rp_pitch_count = 0
    home_cp_pitch_count = 0
    home_sp_scored = 0
    home_rp_scored = 0
    home_pitcher = home_sp


    for inning in innings:
        for top_and_bottom in range(1, 3):
            if top_and_bottom == 1:
                out = 0
                print('-----------------', inning, '회 초 원정팀 공격 -----------------')
                while True:
                    if home_sp_pitch_count > 100 or home_sp_scored > 3:
                        print('rp로 투수 교체')
                        home_sp_pitch_count = 0
                        home_sp_scored = 0
                        home_pitcher = home_rp
                    if home_pitcher == home_rp and (home_rp_pitch_count > 100 or home_rp_scored > 3):
                        print('cp로 투수 교체')
                        home_rp_pitch_count = 0
                        home_rp_scored = 0
                        home_pitcher = home_cp
                    if main():
                        o_res = out_result()[0]
                        out += 1
                        away_hitter_num += 1
                        if away_hitter_num == 10:
                            away_hitter_num = 1
                        print(away_hitter_num, '번 타자, ', o_res)
                        if home_pitcher == home_sp:
                            if o_res == '삼진':
                                home_sp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', home_sp_pitch_count)
                            else:
                                home_sp_pitch_count += pitch_count()
                                print('투구 수 : ', home_sp_pitch_count)
                        if home_pitcher == home_rp:
                            if o_res == '삼진':
                                home_rp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', home_rp_pitch_count)
                            else:
                                home_rp_pitch_count += pitch_count()
                                print('투구 수 : ', home_rp_pitch_count)
                        if home_pitcher == home_cp:
                            if o_res == '삼진':
                                home_cp_pitch_count += pitch_count_case_K()
                                print('투구 수 : ', home_cp_pitch_count)
                            else:
                                home_cp_pitch_count += pitch_count()
                                print('투구 수 : ', home_cp_pitch_count)
                        if out == 3:
                            break
                    else:
                        res = hit_result()[0]
                        if res == '안타':
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:
                                base[0] = 1
                            elif base == [1, 0, 0]:
                                base[1] = 1
                            elif base == [1, 1, 0]:
                                base[2] = 1
                            elif base == [1, 0, 1]:
                                base[1] = 1
                                base[2] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [0, 1, 1]:
                                base[0] = 1
                                base[1] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [0, 1, 0]:
                                base[0] = 1
                                base[2] = 1
                                base[1] = 0
                            elif base == [0, 0, 1]:
                                base[0] = 1
                                base[2] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 1, 1]:
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1

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
                        elif res == '2루타':
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:
                                base[1] = 1
                            elif base == [1, 0, 0]:
                                base[1] = 1
                                base[2] = 1
                                base[0] = 0
                            elif base == [1, 1, 0]:
                                base[2] = 1
                                base[0] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 0, 1]:
                                base[1] = 1
                                base[0] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [0, 1, 1]:
                                base[2] = 0
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2
                            elif base == [0, 1, 0]:
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [0, 0, 1]:
                                base[1] = 1
                                base[0] = 0
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 1, 1]:
                                base[0] = 0
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2

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
                        elif res == '3루타':
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:
                                base[2] = 1
                            elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:
                                base = [0, 0, 1]
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:
                                base = [0, 0, 1]
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2
                            elif base == [1, 1, 1]:
                                base[0] = 0
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
                        elif res == '홈런':
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
                            if base == [0, 0, 0]:
                                away_score += 1
                                inning_away_score += 1
                                if home_pitcher == home_sp:
                                    home_sp_scored += 1
                                if home_pitcher == home_rp:
                                    home_rp_scored += 1
                            elif base == [1, 0, 0] or [0, 1, 0] or [0, 0, 1]:
                                base = [0, 0, 0]
                                away_score += 2
                                inning_away_score += 2
                                if home_pitcher == home_sp:
                                    home_sp_scored += 2
                                if home_pitcher == home_rp:
                                    home_rp_scored += 2
                            elif base == [1, 1, 0] or [1, 0, 1] or [0, 1, 1]:
                                base = [0, 0, 0]
                                away_score += 3
                                inning_away_score += 3
                                if home_pitcher == home_sp:
                                    home_sp_scored += 3
                                if home_pitcher == home_rp:
                                    home_rp_scored += 3
                            elif base == [1, 1, 1]:
                                base = [0, 0, 0]
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
                        else:
                            away_hitter_num += 1
                            if away_hitter_num == 10:
                                away_hitter_num = 1
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
                                away_score += 1
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

                print('3 아웃 change')
                print('-----------------', inning, '회 초 종료,', '원정', away_score, ':', home_score, '홈', '------------------')
                base = [0, 0, 0]
                away_score_list = [inning, inning_away_score]
                print('홈팀,', '이닝,', '점수', away_score_list)
                inning_away_score = 0
                if inning == 9 and home_score > away_score:
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

    jieun = 77
    return jieun

if __name__ == "__main__":
    inning_proc()



