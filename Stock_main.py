import Public_Function
import Naver_top
import Naver_finance
import SearchStockCode
import Naver_F_info
import Chart

(stockNameList, stockCodeList) = Public_Function.getMyList()

def today_upper():
    Public_Function.changeDirectory()

    input_count = 10

    # 상승한애들 이름, code 가져옴.
    item_arr, output_arr = Naver_top.get_today_top_up(int(input_count))

    # 재무상황
    for index, up in enumerate(item_arr) :
        #[23.05.31] 네이버증권 사이트 추가.
        #[23.05.31] 네이버증권 EPS, PER, BPS, PBR
        
        rank = '상한가'+ str(index)+ '_'

        (output_dict, output_sector) = Naver_finance.stock_finance(up['code'], rank, False)

        if type(output_dict) != list  : continue
    
        Naver_top.print_upItem(up['name'], output_sector, rank, output_arr[index])

        #[23.05.31] 네이버증권 종목정보 추가. (0622완료)
        Naver_F_info.stock_info(up['code'], output_sector, rank)

        Naver_finance.print_upItem(up['name'], output_sector, up['code'], rank, output_dict)

        #[23.05.31] 네이버증권> 전자공시
        # 네이버 뉴스 7개
        Naver_top.get_todayNews(up['name'], output_sector, rank, 7)

    Public_Function.changeProjectDirectory()
    return

def today_top_trading():
    Public_Function.changeDirectory()

    input_count = 10

    # 상승한애들 이름, code 가져옴.
    item_arr, output_arr = Naver_top.get_today_top_trading(int(input_count))

    # 재무상황
    for index, top_trading in enumerate(item_arr) :
        #[23.05.31] 네이버증권 사이트 추가.
        #[23.05.31] 네이버증권 EPS, PER, BPS, PBR

        rank = '거래량'+ str(index) +'_'

        (output_dict, output_sector) = Naver_finance.stock_finance(top_trading['code'], rank, False)

        if type(output_dict) != list  : continue
    
        Naver_top.print_upItem(top_trading['name'], output_sector, rank, output_arr[index])

        #[23.05.31] 네이버증권 종목정보 추가. (0622완료)
        Naver_F_info.stock_info(top_trading['code'], output_sector, rank)

        Naver_finance.print_upItem(top_trading['name'], output_sector, top_trading['code'], rank, output_dict)

        #[23.05.31] 네이버증권> 전자공시
        # 네이버 뉴스 7개
        Naver_top.get_todayNews(top_trading['name'], output_sector, rank, 7)

    Public_Function.changeProjectDirectory()
    return


def golden_cross():
    Public_Function.changeDirectory()

    input_count = 40

    # 상승한애들 이름, code 가져옴.
    item_arr, output_arr = Naver_top.get_goldenCross(int(input_count))

    # 재무상황
    for index, top_trading in enumerate(item_arr) :

        rank = '골든크로스'+ str(index) +'_'

        (output_dict, output_sector) = Naver_finance.stock_finance(top_trading['code'], rank, True)

        if type(output_dict) != list  : continue
    
        Naver_F_info.stock_info(top_trading['code'], output_sector, rank)

        Naver_finance.print_upItem(top_trading['name'], output_sector, top_trading['code'], rank, output_dict)

        Naver_top.get_todayNews(top_trading['name'], output_sector, rank, 7)

    Public_Function.changeProjectDirectory()
    return

def getTodayData(stockName, stockCode):
    Public_Function.changeDirectory()

    if stockName == None:
        return

    if stockCode == '':
    
        stockCode = Public_Function.findCode(stockName,stockNameList,stockCodeList)

        if(stockCode== 0) :
            stockCode =  SearchStockCode.searchCode(stockName)

        # 재무상황
    (output_dict, output_sector) = Naver_finance.stock_finance(stockCode, 0, False)

    Naver_F_info.stock_info(stockCode, output_sector, 0)
    Naver_finance.print_upItem(stockName, output_sector, stockCode, 0, output_dict)
    # 오늘 뉴스
    Naver_top.get_todayNews(stockName, output_sector, 0, 5)

    Public_Function.changeProjectDirectory()
    return


def getAllChanges(stockName, stockCode):

    if stockName == None:
        return

    if stockCode == '':
        stockCode = Public_Function.findCode(stockName,stockNameList,stockCodeList)

        if(stockCode== 0) :
            stockCode =  SearchStockCode.searchCode(stockName)

    Naver_finance.stock_allChanges(stockName,stockCode)
    
    return

def ShowStockChart(stockName, stockCode):
    
    if stockName == None:
        return

    if stockCode == '':
        stockCode = Public_Function.findCode(stockName,stockNameList,stockCodeList)

        if(stockCode== 0) :
            stockCode =  SearchStockCode.searchCode(stockName)

    Chart.showChart(stockName,stockCode)

def checkMyList():
    Public_Function.changeTodaySubDirectory()

    # [23.07.05 code도 뽑아오기.]
    for stock_name, stock_code in zip(stockNameList, stockCodeList) :

        (output_dict, output_sector) = Naver_finance.stock_finance(stock_code, 0, True)
        
        if type(output_dict) != list  : continue
    
        Naver_F_info.stock_info(stock_code, output_sector, 0)
        Naver_finance.print_upItem(stock_name, output_sector, stock_code, 0, output_dict)
    
    Public_Function.changeProjectDirectory()
    return