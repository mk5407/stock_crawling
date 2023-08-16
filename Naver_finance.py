import requests
import copy
import csv
import time

from bs4 import BeautifulSoup
from Public_Function import g_encoding

def stock_finance(item_code, rank, check_critria):

   main_url = 'https://finance.naver.com/item/main.naver?code=' + item_code
   raw = requests.get(main_url)
   main_html = BeautifulSoup(raw.text, 'lxml')

   item_name = main_html.select_one('#middle > div.h_company > div.wrap_company > h2 > a').text
   print('%50s' % item_name)

   stock_dict = {}
   dict_array = []
   diff_array = []

   for i in range(4):
      dict_array.append(stock_dict.copy())
      diff_array.append(stock_dict.copy())

   for i in range(1, 5):
      j = i-1

      # 연도
      key = 'YEAR'

      obj_year = main_html.select_one('#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child('+str(i)+')')
      
      # 신규상장주
      if obj_year == None : return

      dict_array[j][key] = obj_year.text.strip()

      arr_row = [1,2,3,4,7,10,11,12,13]

      for k in arr_row:
         obj_key = main_html.select_one('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(' + str(k) + ') > th > strong')
         if obj_key == None : 
            print("신규상장 주식")
            return

         main_key = obj_key.text.strip()
         dict_array[j][main_key] = main_html.select_one('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child('+ str(k) + ')> td:nth-child(' + str(i + 1) + ')').text.strip()

   check_row = [1,2,7]
   fail_array = [0, 0, 0]
   
   for i in range(0, 4):
      diff_array[i] = copy.deepcopy(dict_array[i])

      if i == 0:  continue

      for iter, (prev, cur, diff_key) in enumerate(zip(dict_array[i-1].values(), dict_array[i].values(), diff_array[i])):
         diff_value = 0
         diff_str = 0

         if iter == 0 : continue
         if (cur == '' or cur =='-' ) : diff_str = 0
         elif (prev == '' or prev =='-' ) : diff_str = 0
         else : 
            if '.' in cur :
               diff_value = float(cur.replace(',', '')) - float(prev.replace(',', ''))
               diff_str = round(diff_value, 2)
            else :      
               diff_value = int(cur.replace(',', '')) - int(prev.replace(',', ''))
               diff_str = format(diff_value, ',')

         if(check_critria == True):
            for index, row in enumerate(check_row) :
               if iter == row :
                  if iter == 7 : #PER
                     if (cur == '' or cur =='-' ) : cur = 0
                     if ((type(cur) == str) and ( float(cur) > 30 or float(cur) < 0 )) : fail_array[index]+=1
                  else :
                     if diff_value < 0 : fail_array[index]+=1
               
               if fail_array[index] >= 2 : 
                  print("Critria fail Because {} ".format(diff_key))
                  return
         
         output_str = "{} ({})".format(cur, diff_str)
         diff_array[i][diff_key] = output_str

   return diff_array


def isFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def today_changes(item_name, item_code):

   main_url = 'https://finance.naver.com/item/main.naver?code='+ item_code
   raw = requests.get(main_url)
   main_html = BeautifulSoup(raw.text, 'lxml')

   arr_blinds =  main_html.findAll('span',{'class':"blind"})
   change_keywords = ['현재가','전일대비','퍼센트','전일가','고가','상한가','거래량','시가','저가','거래대금']
   
   index = 0
   today_data = {'종목이름':item_name}

   for info in arr_blinds :
      info_text = info.text.strip('').replace(',','')
      if (info_text.isdigit() == False) and (isFloat(info_text) == False) :
         continue

      key = change_keywords[index]
      
      if info_text.isdigit() == True :
         today_data[key] = format(int(info_text), ',')
      else :
         today_data[key] = format(float(info_text), ',')
         
      index+=1
   
   if today_data['현재가'] < today_data['전일가'] :
      today_data['전일대비'] = '-{}'.format(today_data['전일대비'])
      today_data['퍼센트'] = '-{}'.format(today_data['퍼센트'])

   return today_data

def print_upItem(item_name,item_code, rank, output_dict):  
   out_str = '{}_'.format(rank)+item_name
   f = open(out_str+'.csv', 'a', encoding=g_encoding, newline='')
   wr = csv.writer(f)

   wr.writerow('\n')
   wr.writerow(['네이버증권'])
   wr.writerow(['https://finance.naver.com/item/main.naver?code=' + item_code])
   wr.writerow(['전자공시'])
   wr.writerow(['https://finance.naver.com/item/dart.naver?code=' + item_code])
   wr.writerow('\n')
   wr.writerow(['재무재표요약'])

   for key in output_dict[0]:
      if key == 'EPS(원)':   wr.writerow('\n')

      output_arr = [key,]
      for stock_dict in output_dict:
         output_arr.append(stock_dict[key])

      wr.writerow(output_arr)
   
   f.close()


def stock_allChanges(item_name, item_code):

   all_finance_changes = []
   change_keywords = ['날짜','종가','전일비','등락률','거래량','기관_순매','외_순매','외_보유','외_보유율']

   for i in range(1, 7):

      main_url = 'https://finance.naver.com/item/frgn.naver?code='+ item_code + '&page='+ str(i)

      headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188'}
      r = requests.get(main_url, headers = headers)
      soup = BeautifulSoup(r.text, 'html.parser')
      datas = soup.findAll('tr',{'onmouseover':"mouseOver(this)"})
      
      for day_data in datas:
         
         data_dict = {}
         one_data = day_data.findAll('td')

         for index, data in enumerate(one_data):
            key = change_keywords[index]
            data_dict[key]= data.text.strip()

         all_finance_changes.append(data_dict)

   now = time
   file_name = 'C:\Python\Test\Trading\\' + item_name + '_'+ now.strftime('%Y-%m-%d')+'.csv'

   output_file = open(file_name , 'a', encoding=g_encoding, newline='')
   writer = csv.writer(output_file)    
   writer.writerow(all_finance_changes[0].keys())

   total_count = len(all_finance_changes)

   for day in reversed(all_finance_changes):
      writer.writerow(day.values())

   output_file.close()

   return 0