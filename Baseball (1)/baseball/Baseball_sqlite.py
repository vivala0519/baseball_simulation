import sqlite3
import glob
import pandas as pd


class DBprocess_batter():
    _dbConn = None

    def __init__(self):
        pass

    def getCSV(self, path):
        file = glob.glob(path)

        return file

    def readCSV(self, csvList):
        itemList = []
        for csv in csvList:
            item = pd.read_csv(csv, engine='python', encoding='utf-8', index_col=0, header=0)
            itemList.append(item)

        return itemList


    def connectDB(self):
        self._dbConn = sqlite3.connect('db.sqlite3')


    def createDB(self):
        dbcursor = self._dbConn.cursor()
        dbcursor.execute("create table if not exists Batter \
                                 (id integer primary key autoincrement, player text, year integer, team text, position text,\
                         hit integer, secBase integer, thrBase integer, homeRun integer, fourBalls integer, onBase real)")

        dbcursor.execute("create table if not exists Pitcher \
                                         (id integer primary key autoincrement, player text, year integer, team text, inning real,\
                                 strikeOut real, onBase real)")

    def insert(self, itemList):
        dbcursor = self._dbConn.cursor()

        for index, item in enumerate(itemList):
            data = []

            if index == 0:

                query = "insert into game_batter (player, year, team, position, hit, secBase, thrBase, homeRun, fourBalls, onBase) \
                        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                for row in item.values:
                    data.append(row)

                dbcursor.executemany(query, data)

            else:
                query = "insert into game_pitcher (player, year, team, inning, strikeOut, onBase) \
                                values(?, ?, ?, ?, ?, ?)"

                for row in item.values:
                    data.append(row)

                dbcursor.executemany(query, data)

        self._dbConn.commit()


    def diconnect(self):
        self._dbConn.close()


if __name__ == "__main__":
    obj = DBprocess_batter()
    fileList = obj.getCSV('*.csv')
    csv = obj.readCSV(fileList)
    obj.connectDB()
    obj.insert(csv)

