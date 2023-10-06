import Public_Function
import Naver_top
import Naver_finance
import SearchStockCode
import Naver_F_info

def stock_main():
    

    input_data = input(" 0 (상한가뽑기) or 1 (종목분석) or 2 (거래량전체) or 3 (MyList 검증) :  ")

    if input_data == '0' :
        Public_Function.ChangeDirectory()

        input_count = input(" Top 몇개까지? ")
        
        # 상승한애들 이름, code 가져옴.
        item_arr, output_arr = Naver_top.get_today_top(int(input_count))

        # 재무상황
        for rank, up in enumerate(item_arr) :
            #[23.05.31] 네이버증권 사이트 추가.
            #[23.05.31] 네이버증권 EPS, PER, BPS, PBR

            (output_dict, output_sector) = Naver_finance.stock_finance(up['code'], rank, True)

            if type(output_dict) != list  : continue
        
            Naver_top.print_upItem(up['name'], output_sector, rank, output_arr[rank])

            #[23.05.31] 네이버증권 종목정보 추가. (0622완료)
            Naver_F_info.stock_info(up['code'], output_sector, rank)

            Naver_finance.print_upItem(up['name'], output_sector, up['code'], rank, output_dict)

            #[23.05.31] 네이버증권> 전자공시
            # 네이버 뉴스 7개
            Naver_top.get_todayNews(up['name'], output_sector, rank, 7)

    elif input_data == '3' :

        f = open('stock_list.txt', 'rt', encoding='UTF8')
        Public_Function.ChangeTodaySubDirectory()

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
            
            stock_code = stock_str[1]

            (output_dict, output_sector) = Naver_finance.stock_finance(stock_code, 0, True)
            
            if type(output_dict) != list  : continue
        
            Naver_F_info.stock_info(stock_code, output_sector, 0)
            Naver_finance.print_upItem(stock_name, output_sector, stock_code, 0, output_dict)
        
        f.close()
    else : 
        Public_Function.ChangeDirectory()
        input_stockName = input(" 종목이름은? ")

        stock_Code =  SearchStockCode.searchCode(input_stockName)

        if stock_Code == 0 :
            print("종목이름을 올바르게 입력하시오.")
            exit
        if input_data == '1' :

            # 재무상황
            (output_dict, output_sector) = Naver_finance.stock_finance(stock_Code, 0, False)

            Naver_F_info.stock_info(stock_Code, output_sector, 0)
            Naver_finance.print_upItem(input_stockName, output_sector, stock_Code, 0, output_dict)
            # 오늘 뉴스
            Naver_top.get_todayNews(input_stockName, output_sector, 0, 5)

        elif input_data == '2' :
            Naver_finance.stock_allChanges(input_stockName,stock_Code)
        else :
            print('똑바로 입력하세요!')


stock_main()