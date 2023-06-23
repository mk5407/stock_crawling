import Public_Function
import Naver_top
import Naver_finance
import SearchStockCode

Public_Function.ChangeDirectory()

input_data = input(" 0 (상한가뽑기) or 1 (종목분석) :  ")

if input_data == '0' :

    input_count = input(" Top 몇개까지? ")
    
    # 상승한애들 이름, code 가져옴.
    output_arr = Naver_top.get_today_top(int(input_count))

    # 재무상황
    for rank, up in enumerate(output_arr) :
        Naver_finance.stock_finance(up['code'], rank)

        #[23.05.31] 네이버증권 사이트 추가.
        #[23.05.31] 네이버증권 EPS, PER, BPS, PBR
        #[23.05.31] 네이버증권 종목정보 추가.
        
        #[23.05.31] 네이버증권> 전자공시


        Naver_top.get_todayNews(up['name'], rank, 7)

elif input_data == '1' :

    input_stockName = input(" 종목이름은? ")

    stock_Code =  SearchStockCode.searchCode(input_stockName)

    if stock_Code == 0 :
        print("종목이름을 올바르게 입력하시오.")
        exit

    # 재무상황
    Naver_finance.stock_finance(stock_Code, 0)
    
    # 오늘 뉴스
    Naver_top.get_todayNews(input_stockName, 0, 5)

    # 오늘 상승률?
    # 닥스

else :
    print('똑바로 입력하세요!')
