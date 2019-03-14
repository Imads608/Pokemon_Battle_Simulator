# Mapping Function Codes to Description and Moves
# Puts mapping into a file
import xlrd
import re
import xlsxwriter

def buildFunctionCodeDatabase(fileName):
    # Open Input File
    xlsWorkbook = xlrd.open_workbook(fileName)
    worksheet = xlsWorkbook.sheet_by_index(0)
    numRows = worksheet.nrows
    description = ""

    # Open Output File
    outWorkbook = xlsxwriter.Workbook("../database/Function Codes/Outputs/FCDescription.xlsx")
    outWorksheet = outWorkbook.add_worksheet()
    outWorksheet.write(0, 0, "Function Code Number")
    outWorksheet.write(0, 1, "Description")
    outWorksheet.write(0, 2, "Effect")

    movesFCMap = {}
    currRow = 1
    currCol = 0
    effect = ""
    prevCode = ""
    currCode = ""
    for row in range(0, numRows):
        cellVal1 = str(worksheet.cell(row, 0).value)
        cellVal2 = str(worksheet.cell(row, 1).value)
        cellVal3 = str(worksheet.cell(row, 2).value)

        if (cellVal1 == "Function code"):
            description = str(worksheet.cell(row-1, 0).value)
        else:
            currCode = getFunctionCodeNumber(cellVal1)

        if (currCode != "" and prevCode != "" and prevCode != currCode):
            outWorksheet.write(currRow, currCol, prevCode)
            outWorksheet.write(currRow, currCol+1, description)
            outWorksheet.write(currRow, currCol+2, effect)
            effect = ""
            currRow += 1
            prevCode = currCode
        elif (currCode != ""):
            prevCode = currCode

        if (cellVal2 != "Effect" and cellVal2 != ""):
            effect += cellVal2 + "\n"

        if (cellVal3 != "" and cellVal3 != "Moves with this function code"):
            movesFCMap.update({cellVal3:prevCode})


    outWorksheet.write(currRow, currCol, prevCode)
    outWorksheet.write(currRow, currCol+1, description)
    outWorksheet.write(currRow, currCol+2, effect)

    outWorkbook.close()
    return movesFCMap

def getFunctionCodeNumber(rawVal):
    splitCode = rawVal.split(".")
    code = splitCode[0]
    matchHex = re.search(r'[a-zA-Z]', rawVal)
    codeValid = False

    if (matchHex == None):
        baseNum = 10
    else:
        baseNum = 16

    try:
        int(code, base=baseNum)
        codeValid = True
    except:
        codeValid = False

    if (codeValid == True):
        return str(code)
    return ""

def buildMovesFCMapping(movesFCMap, fileName):
    with open(fileName, 'r') as inPtr:
        allLines = inPtr.readlines()

    outPtr = open("../database/Function Codes/Outputs/movesFCMap.csv", 'w')

    for line in allLines:
        arrayEntry = line.split(",")
        if (arrayEntry[2] != "Move Full Name"):
            functionCode = movesFCMap.get(arrayEntry[2])
            outPtr.write(arrayEntry[0] + "," + arrayEntry[1] + "," + arrayEntry[2] + "," + functionCode + "\n")
        else:
            outPtr.write(arrayEntry[0] + "," + arrayEntry[1] + "," + arrayEntry[2] + "," + arrayEntry[3])

    inPtr.close()
    outPtr.close()

def main():
    functionCodesFileName = "../database/Function Codes/Inputs/Function_Codes.xlsx"
    movesFCMap = buildFunctionCodeDatabase(functionCodesFileName)
    movesFCFileName = "../database/Function Codes/Inputs/Moves Function Code Translation.csv"
    buildMovesFCMapping(movesFCMap, movesFCFileName)

    return

if __name__ == "__main__":
    main()
