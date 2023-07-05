import Public_Function
import Naver_top
import Naver_finance
import SearchStockCode
import Naver_F_info

def tracking_stock_main() :

    f = open('stock_list.txt', 'r')
    
    all_changes=[]
    line_num = 1
    stock_name = f.readline().replace('\n','')

    while stock_name:
        stock_code =  SearchStockCode.searchCode(stock_name)
        all_changes.append(Naver_finance.today_changes(stock_name, stock_code))

        stock_name = f.readline().replace('\n','')
        line_num += 1
    f.close()



tracking_stock_main()