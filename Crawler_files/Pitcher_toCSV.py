from selenium import webdriver
import urllib.request
import urllib.parse
import pandas as pd
import re


def get_url(url, enc='utf-8'):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)

    if response.getcode() == 200:
        data = response.read()

        return data
    else:
        return None

def get_crawl(year, teamName):

    playerStat = []

    url = "http://www.statiz.co.kr/stat.php?opt=0&sopt=0&re=1&ys=%s&ye=%s" \
          "&se=0&te=%s&tm=&ty=0&qu=auto&po=0&as=&ae=&hi=&un=&pl=&da=2&o1=FIP" \
          "&de=0&o2=WAR&lr=0&tr=&cv=&ml=1&sn=30&si=&cn="\
          % (year, year, urllib.parse.quote_plus(teamName))

    browser = webdriver.Chrome('C:\BigDeep\ChromeDriver\chromedriver.exe')
    browser.implicitly_wait(2)

    browser.get(url)

    selectedTr = browser.find_elements_by_css_selector('table#mytable tr')[2:]

    for index, tr in enumerate(selectedTr):
        tdList = tr.text.split(' ')
        # print(tdList)
        if (ord("0") > ord(tdList[0][0])) or (ord("9") < ord(tdList[0][0])) :
            continue

        for td in tdList:
            if td == '':
                td = str(0)

        playerStat.append(tdList[0:17])

    print(playerStat)

    browser.close()
    return playerStat

def main():
    yearScope = range(2015, 2019)
    teamNameList = ['두산','삼성','NC','넥센','SK','한화','LG','롯데','KIA','kt', '히어로즈']

    columnList = ['순', '이름', '팀', 'FIP', '출장', '이닝', 'ERA', 'FIP',
                  'K/9', 'BB/9', 'HR/9', 'K/BB', 'PFR', 'BIPA', 'LOB%',
                  '타율', '출루율']

    for year in yearScope:
        for teamName in teamNameList:
            recordList = get_crawl(year, teamName)
            if len(recordList) != 0:
                # print(recordList)
                recordTable = pd.DataFrame(recordList, columns=columnList)
                recordTable.to_csv(str(year) + str(teamName) + '_pitcher.csv', encoding="utf-8", mode="w")

                del recordTable
            del recordList

if __name__ == "__main__":
    main()