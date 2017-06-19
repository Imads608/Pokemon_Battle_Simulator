import re
from pandas import *
import xlrd


def getDict(fileName):
    moveDatabase = {}
    wb = xlrd.open_workbook(fileName)
    sh = wb.sheet_by_index(0)
    for i in range(138):
        matchNum = r'[0-9]+'
        numMatched = re.search(matchNum, str(sh.cell(i,0).value))
        if (numMatched != None):
            strKey = numMatched.group()
        else:
            strKey = sh.cell(i,0).value
        moveDatabase.update({strKey:sh.cell(i,1).value})

    return moveDatabase

def getMoves(fileName):
    with open(fileName, 'r') as moves:
        allLines = moves.readlines()
    database = {}

    for line in allLines:
        data = line.split(",")
        csvdata = data[1:13]
        moveDescription = data[13:]
        description = ""
        for partDescription in moveDescription:
            description += partDescription
        tupleData = (csvdata[0], csvdata[1], csvdata[2], csvdata[3], csvdata[4], csvdata[5], csvdata[6], csvdata[7], csvdata[8],
                     csvdata[9], csvdata[10],csvdata[11], description)
        database.update({data[0]:tupleData})

    return database

if __name__ == "__main__":
    functionCodes = getDict("moveFunctionCodes.xls")
    moveDatabase = getMoves("Pokémon Essentials v16 2015-12-07/PBS/moves.txt")
    print(moveDatabase)