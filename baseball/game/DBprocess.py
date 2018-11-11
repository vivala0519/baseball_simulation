from .models import Batter, Pitcher


class DBprocess():

    home_batters = []
    away_batters = []

    home_pitchers = []
    away_pitchers = []

    positionDict = {'포수': 'C', '1루수': '1B', '2루수': '2B', '3루수': '3B',
                    '유격수': 'SS', '좌익수': 'LF', '중견수': 'CF',
                    '우익수': 'RF', '지명타자': 'DF'}

    """
    player리스트의 세부 요소는 terminal에 출력된다.
    """

    def __init__(self):
        pass


    def getBattersAndPitchers(self, playerList):

        for index, player in enumerate(playerList):
            print("player = ", player)
            if index <= 11:
                if player[3] == '타자':
                    self.home_batters.append(player)
                else:
                    self.home_pitchers.append(player)
            else:
                if player[3] == '타자':
                    self.away_batters.append(player)
                else:
                    self.away_pitchers.append(player)


    def getBatterStat(self, batters):

        batters_stat = []

        for player in batters:
            stat = Batter.objects.filter(year=int(player[1])).filter(team=player[2])\
                    .filter(position=self.positionDict[player[4]]).filter(player=player[5]).values()

            batters_stat.append(stat)

        return batters_stat


    def getPitchersStat(self, pitchers):

        pitchers_stat = []

        for player in pitchers:
            stat = Pitcher.objects.filter(year=player[1]).\
                                filter(team=player[2]).filter(player=player[5]).values()

            pitchers_stat.append(stat)

        return pitchers_stat