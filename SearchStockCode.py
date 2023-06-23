import pandas as pd
import requests

def searchCode (stockName):
    url = requests.get('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13',verify=False).text
    df = pd.read_html(url, header=0)[0]
    stock_list = df[['종목코드', '회사명']]

    df = df.rename(columns={'종목코드': 'code', '회사명': 'company'})
    stock_code_list = df.code.map('{:06d}'.format)

    for stock, stock_Code6  in zip( stock_list.values, stock_code_list.values)  :
        if( stock[1] == stockName):
            return stock_Code6

    return 0