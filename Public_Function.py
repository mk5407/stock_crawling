import os
import time
import platform
import SearchStockCode

# check platform 
# Linux: Linux
# Mac: Darwin
# Windows: Windows

g_os = platform.system()
g_encoding=''
if g_os=='Windows': g_encoding='ANSI'
else : g_encoding='utf-8'

g_projDir=os.getcwd()

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def changeProjectDirectory():
    os.chdir(g_projDir)

def changeDirectory() :
    now = time
    directory = 'C:\Python\Test\Daily\\'+ now.strftime('%Y-%m-%d')
    createDirectory(directory)
    os.chdir(directory)

def changeGoldenDirectory() :
    now = time
    directory = 'C:\Python\Test\GoldenCross\\'+ now.strftime('%Y-%m-%d')
    createDirectory(directory)
    os.chdir(directory)

def changeTodaySubDirectory() :
    now = time
    directory = 'C:\Python\Test\Verify\\'+ now.strftime('%Y-%m-%d')
    createDirectory(directory)
    os.chdir(directory)

def getMyList(fileName):
    f = open(fileName, 'rt', encoding='UTF8')
    output_file = open('stock_study.txt', 'a', encoding=g_encoding, newline='')

    all_stockNames=[]
    all_stockCodes=[]

    line_num = 1
    f.readline()

    # [23.07.05 code도 뽑아오기.]
    while True:
        line = f.readline()

        if not line : break

        stock_str = line.strip().split(',')
        stock_name = stock_str[0]

        if stock_name == '': continue
        if stock_name.find('@') != -1 : continue
        
        stock_code = 0
        
        if len(stock_str) == 1 : 
            stock_code = SearchStockCode.searchCode(stock_name)
            output_file.write('{},{}\n'.format(stock_name,stock_code))
        else :
            stock_code = stock_str[1]
            
        all_stockNames.append(stock_name)
        all_stockCodes.append(stock_code)

        line_num += 1

    f.close()
    output_file.close()

    return all_stockNames, all_stockCodes


def findCode(stockName, stockNameList, stockCodeList) :

    for index, name in enumerate(stockNameList) :
        if(stockName==stockNameList[index]) :
            return stockCodeList[index] 

    return 0