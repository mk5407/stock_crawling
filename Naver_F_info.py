import requests
import copy
import csv
import time

from bs4 import BeautifulSoup
from Public_Function import g_encoding

def stock_info(item_code, item_sector, rank):

   main_url = 'https://finance.naver.com/item/coinfo.naver?code=' + item_code
   raw = requests.get(main_url)
   main_html = BeautifulSoup(raw.text, 'lxml')

   item_name = main_html.select_one('#middle > div.h_company > div.wrap_company > h2 > a').text
   #wrapper > div:nth-child(6) > div.cmp_comment > ul > li:nth-child(1)
   #wrapper > div:nth-child(6) > div.cmp_comment > ul > li:nth-child(2)

   arr_infos =  main_html.findAll('div',{'id':"summary_lyr"})
   output_arr = []
   for info in arr_infos :
      find_text = info.find('div',{'id','summary_info'}).text.strip()
      output_arr.append(''.join(find_text))
   now = time
   out_str = '{}_{}({})'.format(rank,item_name,item_sector)
   f = open(out_str+'.csv', 'a', encoding=g_encoding, newline='')
   wr = csv.writer(f)
   wr.writerow(output_arr)

   f.close()