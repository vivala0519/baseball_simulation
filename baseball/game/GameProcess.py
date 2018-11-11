from random import choices


class Game():
    home_score = 0
    away_score = 0
    inning_home_score = 0
    inning_away_score = 0
    batter_stat = []
    pitcher_stat = []


    # Game객체를 이용하기 위해서는 반드시 setStats 메소드로 필드를 초기화해야한다.
    def setStats(self, batter_stat, pitcher_stat):
        self.batter_stat = batter_stat
        self.pitcher_stat = pitcher_stat


    def hit_result(self):  # 안타 결과(안타, 2루타, 3루타, 홈런, 볼넷 출력)

        hit = self.batter_stat[5] + self.batter_stat[9]
        BB = self.batter_stat[9]

        hit_one = self.batter_stat[5] - self.batter_stat[6] - self.batter_stat[7] \
                  - self.batter_stat[8]

        hit_two = self.batter_stat[6]

        hit_three = self.batter_stat[7]

        homerun = self.batter_stat[8]

        hit_kind = ['안타', '2루타', '3루타', '홈런', '볼넷']
        run_rate = [hit_one / hit, hit_two / hit, hit_three / hit, homerun / hit, BB / hit]

        hit_def = choices(hit_kind, run_rate)

        return hit_def

    def out_result(self):  # 아웃 결과 (삼진, 뜬공, 땅볼 중 출력

        out_kind = ['삼진', '땅볼아웃', '뜬공아웃']
        out_rate = [0.3333333334, 0.3333333333, 0.3333333333]
        # 특정 년도 이전에는 땅볼, 뜬공 기록이 없기에 각각 1/3 확률로 나오도록 설정

        out_def = choices(out_kind, out_rate)
        # print('아웃! : ' + out_def[0])
        return out_def

    def main(self, pitcher_league_obp, batter_league_obp):  # 타자 투수 대결 결과 (안타, 아웃 중 출력)

        pitcher = self.pitcher_stat[6]
        batter = self.batter_stat[10]
        batter_oz = batter / (1 - batter)
        pitcher_oz = (1 - pitcher) / pitcher
        pitcher_league_obp_oz = (1 - pitcher_league_obp) / pitcher_league_obp

        batter_league_obp_oz = batter_league_obp / (1 - batter_league_obp)
        total_league_OBP_avg = 0.340
        total_league_OBP_avg_oz = total_league_OBP_avg / (1 - total_league_OBP_avg)
        OR = ((batter_oz / batter_league_obp_oz) / (pitcher_oz / pitcher_league_obp_oz)) * total_league_OBP_avg_oz
        result = round(OR / (1 + OR), 3)

        # print('타자가 투수를 상대로 출루를 할 확률 : ', result)

        hit_or_out = ['안타', '아웃']
        hit_rate = [result, 1 - result]

        total_result = choices(hit_or_out, hit_rate)

        if total_result[0] == '안타':
            return False
        else:
            return True

    # 고정값
    def pitch_count(self):  # 투구 수 결과 (투구 수 1 ~ 10개 중 출력)
        pitch_count_kind = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        hit_count_rate = [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.07, 0.07, 0.07, 0.07]
        pitch_count_def = choices(pitch_count_kind, hit_count_rate)
        pitch_count = int(pitch_count_def[0])

        return pitch_count

    # 고정값
    def pitch_count_case_BB(self):  # 볼넷일 시 투구수 결과 (투구 수 3 ~ 10개 중 출력)

        pitch_count_kind = [4, 5, 6, 7, 8, 9, 10]
        hit_count_rate = [0.16, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14]
        pitch_count_def = choices(pitch_count_kind, hit_count_rate)
        pitch_count = int(pitch_count_def[0])

        return pitch_count

    # 고정값
    def pitch_count_case_K(self):  # 삼진일 시 투구수 결과 (투구 수 3 ~ 10개 중 출력)

        pitch_count_kind = [3, 4, 5, 6, 7, 8, 9, 10]
        hit_count_rate = [0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125]
        pitch_count_def = choices(pitch_count_kind, hit_count_rate)
        pitch_count = int(pitch_count_def[0])

        return pitch_count


    # 연도별로 리그 출루율 가져오는 메서드
    def get_league_obp(self):
        obpStr = '82 - 0.338,\
                83 - 0.323,\
                84 - 0.326,\
                85 - 0.332,\
                86 - 0.322,\
                87 - 0.335,\
                88 - 0.336,\
                89 - 0.336,\
                90 - 0.339,\
                91 - 0.336,\
                92 - 0.345,\
                93 - 0.320,\
                94 - 0.327,\
                95 - 0.322,\
                96 - 0.327,\
                97 - 0.334,\
                98 - 0.331,\
                99 - 0.352,\
                00 - 0.347,\
                01 - 0.357,\
                02 - 0.335,\
                03 - 0.345,\
                04 - 0.347,\
                05 - 0.342,\
                06 - 0.330,\
                07 - 0.340,\
                08 - 0.342,\
                09 - 0.358,\
                10 - 0.351,\
                11 - 0.344,\
                12 - 0.334,\
                13 - 0.350,\
                14 - 0.365,\
                15 - 0.357,\
                16 - 0.364,\
                17 - 0.353,\
                18 - 0.353'

        arr = obpStr.split(',')
        obp_book = {}

        for item in arr:
            itemSplit = item.split('-')
            obp_book[itemSplit[0].strip()] = float(itemSplit[1].strip())

        return obp_book


    # 선수 기록에 리그 출루율을 더하고 Queryset에서 List로 형변환한다.
    def set_league_obp_to_player(self, playerList, obp_book):

        statList = []

        try:
            for player in playerList:
                valueList = list(player.values_list()[0])
                year = valueList[2]
                valueList.append(obp_book[str(year)[2:]])

                statList.append(valueList)

        except Exception as e:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> error >>>>>>>>>>>", e)

        print("============================= statList ================================")
        print(statList)
        print("============================= statList ================================")

        return statList


    # 주자가 있는 베이스를 배열로 반환한다.
    def findOccupiedBase(self, base):

        # 'item == 1'은 주자가 있는 베이스를 의미한다. 인덱스는 0부터 시작하므로 1을 더해준 값을 사용한다.
        base_occupied = [index + 1 for index, item in enumerate(base) if item == 1]

        return base_occupied

    # base_occupied 자리의 파라미터는 주자가 있는 베이스를 요소로 가진다.
    # ex) 1, 3루에 주자 있을 경우 [1, 3], 3루에만 있을 경우 [3], 주자 없는 경우 빈 배열 []
    # 안타지만 볼넷이 아닌 경우
    def countingScoreWithoutBB(self, base_occupied, hit, score):

        base = [0, 0, 0]
        hit_kind = {'안타': 1, '2루타': 2, '3루타': 3, '홈런': 4}

        for index, item in enumerate(base_occupied):
            if item + hit_kind[hit] <= 3:  # True면 base 세팅만, False면 득점 후 base 세팅
                base[item + hit_kind[hit] - 1] = 1  # 원래 베이스에 있던 사람 이동
            else:
                score += 1

        # 이제 막 출루한 사람의 위치 조정하는 부분
        if hit != '홈런':
            base[hit_kind[hit] - 1] = 1
        else:
            score += 1  # 솔로 홈런일 경우, 위치 조정하면서 점수 증가
            base = [0, 0, 0]

        return base, score


    # 현재 실제의 베이스를 가져와야 한다.
    # 볼넷인 경우
    def countingScoreOnBB(self, base, base_occupied, score):
        len_of_base_occupied = len(base_occupied)

        # 만루일 경우
        if len_of_base_occupied == 3:
            score += 1
            base_occupied_on_base = [0, 0, 0]
            return base_occupied_on_base, score

        # 만루가 아닐 경우
        if base[0] == 0:
            base[0] = 1
            return base, score
        else:
            if base[1] == 1:
                base[2] = 1
                return base, score

            base[1] = 1
            return base, score







