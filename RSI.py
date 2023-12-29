import pandas as pd
from pandas import DataFrame
from pandas_ta.utils import get_offset, verify_series
from pandas_ta.utils import recent_maximum_index, recent_minimum_index
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
import warnings
import datetime
import finplot as fplt
import time
from datetime import datetime, timedelta

import matplotlib.ticker as ticker

warnings.filterwarnings('ignore')

# def SMA(data,period = 30, column = 'Close') :
#     return data[column].rolling(window = period).mean()

def RSI(df):
    diff = df['Close'].diff(1).values
    gains = diff
    losses = -diff

    if len(gains) < 15 : return None

    with np.errstate(invalid='ignore'):
        gains[(gains<0)|np.isnan(gains)] = 0.0
        losses[(losses<=0)|np.isnan(losses)] = 1e-10 # we don't want divide by zero/NaN
    n = 14
    m = (n-1) / n
    ni = 1 / n
    g = gains[n] = np.nanmean(gains[:n])
    l = losses[n] = np.nanmean(losses[:n])
    gains[:n] = losses[:n] = np.nan
    for i,v in enumerate(gains[n:],n):
        g = gains[i] = ni*v + m*g
    for i,v in enumerate(losses[n:],n):
        l = losses[i] = ni*v + m*l
    rs = gains / losses
    df['rsi'] = 100 - (100/(1+rs))

    return df

# def RSI(data, period = 14, column = 'Close') :
#     delta = data[column].diff(1)
#     delta = delta.dropna()
    
#     up = delta.copy()
#     down = delta.copy()
#     up[up <0] =0
#     down[down>0] = 0
#     data['up'] = up
#     data['down'] = down
    
#     AVG_Gain = SMA(data, period, column = 'up')
#     AVG_Loss = abs(SMA(data,period,column = 'down'))
#     RS = AVG_Gain / AVG_Loss
    
#     RSI = 100.0 - (100.0 / (1.0+RS))
#     data['RSI'] = RSI
    
#     return data

def getRSI_Value(item_code):
    now = datetime.now()
    end_time = now + timedelta(days=1)
    start_time = (end_time+timedelta(days=-90)).strftime('%Y-%m-%d')
    
    df = yf.download(tickers = (item_code +'.KQ'), start=start_time, end=end_time.strftime('%Y-%m-%d'))
    if df.empty : 
        df = yf.download(tickers = (item_code +'.KS'), start=start_time, end=end_time.strftime('%Y-%m-%d'))


    df = RSI(df)

    if df is None : return 0

    while(True):
        end_str = end_time.strftime('%Y-%m-%d')
        
        try :
            rsi_value=df['rsi'][end_str]
            return round(rsi_value,2)
        except:
            end_time=end_time+timedelta(days=-1)

#getRSI_Value('005930')
