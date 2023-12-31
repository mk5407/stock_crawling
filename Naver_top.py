import requests
import copy
import os
import csv
import time
import string

from bs4 import BeautifulSoup
from Public_Function import g_encoding

def get_today_top_up(count):
    URL = 'https://finance.naver.com/'
    raw = requests.get(URL)
    html = BeautifulSoup(raw.text,'lxml')
    units_up =  html.select('#_topItems2>tr')  # 오늘 상한가 종목들 전부 다 가져오는거

    item_arr = []

    out_dict = [] 
    out_arr = []
    for i in range(count):
      out_arr.append(out_dict.copy())

    now = time
    print('=====금일 상한가 종목=====')
    print()

    for index, unit in enumerate(units_up[:count]):
        title_up = unit.select_one('#_topItems2 > tr> th > a').text
        price_up = unit.select_one('#_topItems2 > tr> td')
        up = unit.select_one('#_topItems2 > tr > td:nth-child(3)').text
        up = up.replace('상한가', '↑')

        percent_up = unit.select_one('#_topItems2 > tr> td:nth-child(4)')
        
        item_code = unit.select_one('#_topItems2 > tr> th > a')['href'].split('=')[1]
        
        out_arr[index].append(['종목 이름',title_up])
        out_arr[index].append(['한 주당 가격', price_up.text])
        out_arr[index].append(['전날 대비 가격 변동',up])
        out_arr[index].append(['전날 대비 등락',percent_up.text])

        print('\n')

        item_dict = {'name':title_up, 'code':item_code, }
        item_arr.append(copy.deepcopy(item_dict))

    return item_arr, out_arr

def get_today_top_trading(count):
    URL = 'https://finance.naver.com/'
    raw = requests.get(URL)
    html = BeautifulSoup(raw.text,'lxml')
    units_up =  html.select('#_topItems1>tr')  # 오늘 거래량 최대종목 전부 다 가져오는거

    item_arr = []

    out_dict = [] 
    out_arr = []
    for i in range(count):
      out_arr.append(out_dict.copy())

    now = time
    print('=====금일 거래량 상위 종목=====')
    print()

    for index, unit in enumerate(units_up[:count]):
        title_up = unit.select_one('#_topItems1 > tr> th > a').text
        price_up = unit.select_one('#_topItems1 > tr> td')
        diff = unit.select_one('#_topItems1 > tr > td:nth-child(3)').text
        # up = up.replace('상한가', '↑')

        percent_up = unit.select_one('#_topItems1 > tr> td:nth-child(4)')
        
        item_code = unit.select_one('#_topItems1 > tr> th > a')['href'].split('=')[1]
        
        out_arr[index].append(['종목 이름',title_up])
        out_arr[index].append(['한 주당 가격', price_up.text])
        out_arr[index].append(['전날 대비 가격 변동',diff])
        out_arr[index].append(['전날 대비 등락',percent_up.text])

        print('\n')

        item_dict = {'name':title_up, 'code':item_code, }
    

        item_arr.append(copy.deepcopy(item_dict))

    return item_arr, out_arr

def get_goldenCross(count):
    URL = 'https://finance.naver.com/sise/item_gold.naver'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'}
    raw = requests.get(URL, headers = headers)
    html = BeautifulSoup(raw.text,'lxml')
    golden_list = html.findAll('a', 'tltle')
    item_arr = []
    out_dict = [] 
    out_arr = []
    now = time
    
    for i in range(count):
      out_arr.append(out_dict.copy())

    print('=====골든크로스 체크=====')
    print()

    for index, unit in enumerate(golden_list[:count]):
        item_name = unit.text
        item_code = unit.get('href').split('=')[1]

        item_dict = {'name':item_name, 'code':item_code, }

        item_arr.append(copy.deepcopy(item_dict))

    return item_arr, out_arr

def get_todayNews(item_name, item_sector, rank, count) :

    news_up = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query='+ item_name
    raw2 = requests.get(news_up)
    html2= BeautifulSoup(raw2.text,'lxml')
    news_up_box = html2.find('div',{'class':'group_news'})
    news_up_list = news_up_box.find_all('div',{'class':'news_area'}) # 박스

    now = time
    out_str = '{}_{}({})'.format(rank,item_name,item_sector)
    f = open(out_str+'.csv', 'a', encoding=g_encoding, newline='')
    wr = csv.writer(f)
    wr.writerow('\n\n')
    wr.writerow(['관련된 뉴스기사'])
    
    for new in news_up_list[:count]:
        new_title_up = new.find('a',{'class' : 'news_tit'})

        try:
            wr.writerow([new_title_up.text])
            link_up = new.find('a',{'class' : 'api_txt_lines dsc_txt_wrap'})

            new_up = link_up['href']
            wr.writerow([new_up])
            wr.writerow('\n')
        except UnicodeEncodeError:   continue
        
    f.close()

def print_upItem(item_name, item_sector, rank, output_str): 

    out_str = '{}_{}({})'.format(rank,item_name,item_sector)
    f = open(out_str+'.csv', 'a', encoding=g_encoding, newline='')
    wr = csv.writer(f)

    for str in output_str : 
        print(str)
        wr.writerow(str)

    f.close()