import Public_Function
import Naver_top
import Naver_finance
import SearchStockCode
import Naver_F_info
import csv
import time
import os.path

from Public_Function import g_encoding

def tracking_stock_main(today_tracking, stock_tracking) :

    f = open('stock_list.txt', 'rt', encoding='UTF8')
    Public_Function.ChangeDirectory()

    all_changes=[]
    all_stockcodes=[]

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

        all_stockcodes.append(stock_code)
        all_changes.append(Naver_finance.today_changes(stock_name, stock_code))

        line_num += 1
    
    f.close()

    now = time
# 해당 날짜에 정렬
    if today_tracking :
        file_name = 'C:\Python\Test\Tracking_List\\'+ now.strftime('%Y-%m-%d') +'.csv'

        output_file = open(file_name, 'a', encoding=g_encoding, newline='')
        writer = csv.writer(output_file)    
        writer.writerow(all_changes[0].keys())

        for stock in all_changes:
            writer.writerow(stock.values())

        output_file.close()

   # 종목별로 출력추가
    if stock_tracking :
        for stock, stock_code in zip(all_changes, all_stockcodes):
            stock_name = stock['종목이름']
            file_name = 'C:\Python\Test\Tracking\\' + stock_name

            file_exist = os.path.isfile(file_name+'.csv')

            stock_file = open(file_name+'.csv', 'a', encoding=g_encoding, newline='')
            daily_writer = csv.writer(stock_file)

            if file_exist == False :
                daily_writer.writerow(['https://finance.naver.com/item/fchart.naver?code=' + stock_code])
                daily_writer.writerow(all_changes[0].keys())

            # 종목이름대신 날짜로 입력
            stock['종목이름'] = now.strftime('%Y-%m-%d')
            daily_writer.writerow(stock.values())
            stock_file.close()

tracking_stock_main(True, False)