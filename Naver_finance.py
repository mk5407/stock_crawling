import requests
import copy
import csv
import time

from bs4 import BeautifulSoup

def stock_finance(item_code, rank):

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

      obj_year = dict_array[j][key] = main_html.select_one('#content > div.section.cop_analysis > div.sub_section > table > thead > tr:nth-child(2) > th:nth-child('+str(i)+')')
      
      # 신규상장주
      if obj_year == None : return

      dict_array[j][key] = obj_year.text.strip()

      for k in range(1, 5):
         obj_key = main_html.select_one('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child(' + str(k) + ') > th > strong')
         if obj_key == None : return

         main_key = obj_key.text.strip()
         dict_array[j][main_key] = main_html.select_one('#content > div.section.cop_analysis > div.sub_section > table > tbody > tr:nth-child('+ str(k) + ')> td:nth-child(' + str(i + 1) + ')').text.strip()

   for i in range(0, 4):
      diff_array[i] = copy.deepcopy(dict_array[i])

      if i == 0:  continue

      for iter, (prev, cur, diff_key) in enumerate(zip(dict_array[i-1].values(), dict_array[i].values(), diff_array[i])):
         diff = 0
         if iter == 0 : continue
         if (cur == '') : diff = 0
         else : 
            if iter == 4 :
               diff = float(cur.replace(',', '')) - float(prev.replace(',', ''))
               diff = round(diff, 2)
            else:      
               diff = int(cur.replace(',', '')) - int(prev.replace(',', ''))
               diff = format(diff, ',')

         output_str = "{} ({})".format(cur, diff)
         diff_array[i][diff_key] = output_str

   now = time
   out_str = '{}_'.format(rank)+item_name
   f = open(out_str+'.csv', 'a', encoding='utf-8', newline='')
   wr = csv.writer(f)

   wr.writerow('\n')
   wr.writerow(['재무재표요약'])

   for key in diff_array[0]:
      output_arr = [key,]
      for stock_dict in diff_array:
         output_arr.append(stock_dict[key])

      wr.writerow(output_arr)

   f.close()

   # for key in diff_array[0]:
   #    strFormat = '%-20s'
   #    strForma2 = '%-30s'
   #    str = strFormat % (key)
   #    for stock_dict in diff_array:
   #       str += strForma2 % (stock_dict[key])
   #     wr.writerow(str)

