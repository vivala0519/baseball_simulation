from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import pandas as pd
from selenium import webdriver


def get_crawl(year, teamName):

    playerStat = []

    url = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=0&ys=%d&ye=%d&se=0" \
          "&te=%s&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=1&o1=WAR_ALL_ADJ" \
          "&o2=TPA&de=1&lr=0&tr=&cv=&ml=1&sn=30&si=&cn="\
          % (year, year, urllib.parse.quote_plus(teamName))

    browser = webdriver.Chrome('C:\BigDeep\ChromeDriver\chromedriver.exe')
    browser.implicitly_wait(2)

    browser.get(url)

    selectedTr = browser.find_elements_by_css_selector('table#mytable tr')

    for index, item in enumerate(selectedTr):
        # print("item = ", item.text)
        if len(item.text) <= 5:
            break

        if (item.find_elements_by_css_selector('th')):
            continue

        itemSplit = item.text.split(' ')
        refine = [x for x in itemSplit if x]
        # print(refine)
        if ord(str(0)) <= ord(refine[0][0]) <= ord(str(9)):
            print(refine)
            playerStat.append(refine)

    return playerStat

def main():
    # yearScope = range(2014, 2019)
    yearScope = range(2015, 2019)
    teamNameList = ['두산','삼성','NC','넥센','SK','한화','LG','롯데','KIA','kt', '히어로즈']
    columnList = ['순', '이름', '팀', 'WAR+', 'G', '타석', '타수', '득점', '안타', '2타',
                  '3타', '홈런', '루타', '타점', '도루', '도실', '볼넷',
                  '사구', '고4', '삼진', '병살', '희타', '희비', '타율',
                  '출루율', '장타', 'OPS', 'wOBA', 'wRC+', 'WAR', 'WPA']


    for year in yearScope:
        for teamName in teamNameList:
            recordList = get_crawl(year, teamName)
            if len(recordList) != 0:
                recordTable = pd.DataFrame(recordList, columns=columnList)

                if len(recordTable) == 0:
                    continue

                print(recordTable)
                recordTable.to_csv(str(year) + str(teamName) + '_batter.csv', encoding="utf-8", mode="w")

                del recordTable
            del recordList

if __name__ == "__main__":
    main()