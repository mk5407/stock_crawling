import requests
import copy
import os
import csv
import time
import string

from bs4 import BeautifulSoup

def get_today_top(count):
    URL = 'https://finance.naver.com/'
    raw = requests.get(URL)
    html = BeautifulSoup(raw.text,'lxml')
    units_up =  html.select('#_topItems2>tr')  # 오늘 상한가 종목들 전부 다 가져오는거

    item_arr = []
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

        out_str = '{}_'.format(index) + title_up
        f = open(out_str+'.csv', 'a', encoding='utf-8', newline='')
        wr = csv.writer(f)
        
        out_arr=[]
        out_arr.append(['종목 이름',title_up])
        out_arr.append(['한 주당 가격', price_up.text])
        out_arr.append(['전날 대비 가격 변동',up])
        out_arr.append(['전날 대비 등락',percent_up.text])

        for str in out_arr : 
            print(str)
            wr.writerow(str)    

        print('\n')

        f.close()

        item_dict = {'name':title_up, 'code':item_code, }
        item_arr.append(copy.deepcopy(item_dict))

    return item_arr

def get_todayNews(item_name, rank, count) :

    news_up = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query='+ item_name
    raw2 = requests.get(news_up)
    html2= BeautifulSoup(raw2.text,'lxml')
    news_up_box = html2.find('div',{'class':'group_news'})
    news_up_list = news_up_box.find_all('div',{'class':'news_area'}) # 박스

    now = time
    out_str = '{}_'.format(rank) + item_name
    f = open(out_str+'.csv', 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow('\n\n')
    wr.writerow(['관련된 뉴스기사'])
    
    for new in news_up_list[:count]:
        new_title_up = new.find('a',{'class' : 'news_tit'})
        wr.writerow([new_title_up.text])
        link_up = new.find('a',{'class' : 'api_txt_lines dsc_txt_wrap'})

        new_up = link_up['href']
        wr.writerow([new_up])
        wr.writerow('\n')

    f.close()