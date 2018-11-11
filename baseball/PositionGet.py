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


    def selectDB(self, csv):
        dbcursor = self._dbConn.cursor()

        position_batter = []
        list = []

        for item in csv:
            if position_batter.count(item.포지션) > 0:
                continue
            print(item.포지션.values)
            position_batter.append(item.포지션)

        print(position_batter)

    def diconnect(self):
        self._dbConn.close()


if __name__ == "__main__":
    obj = DBprocess_batter()
    csv = obj.getCSV('Batter.csv')
    db = obj.readCSV(csv)
    obj.connectDB()
    obj.selectDB(db)
    obj.diconnect()

