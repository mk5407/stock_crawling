import Public_Function
import Naver_top
import Naver_finance
import SearchStockCode
import Naver_F_info
import csv
import time


from Public_Function import g_encoding


def tracking_stock_main() :

    f = open('stock_list.txt', 'rt', encoding='UTF8')
    Public_Function.ChangeDirectory()

    all_changes=[]
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

        all_changes.append(Naver_finance.today_changes(stock_name, stock_code))

        line_num += 1
    
    f.close()


   # 해당 날짜에 정렬
   # 종목별로 출력추가필요.[2023.07.12]
    now = time
    output_file = open(now.strftime('%Y-%m-%d')+'.csv', 'a', encoding=g_encoding, newline='')
    writer = csv.writer(output_file)

    writer.writerow(all_changes[0].keys())

    for stock in all_changes:
       writer.writerow(stock.values())

    output_file.close()

tracking_stock_main()