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

def plot_heikin_ashi(df, ax):
    df[['Open','Close','High','Low']].plot(ax=ax, kind='candle')
    fplt.plot(df.Close.rolling(50).mean())
    fplt.plot(df.Close.rolling(200).mean())

def plot_heikin_ashi_volume(df, ax):
    df[['Open','Close','Volume']].plot(ax=ax, kind='volume')

def plot_rsi(df, ax):
    diff = df['Close'].diff(1).values
    gains = diff
    losses = -diff

    if len(gains) < 14 : return None

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
    df.rsi.plot(ax=ax, legend='RSI')
    fplt.set_y_range(0, 100, ax=ax)
    fplt.add_band(30, 70, ax=ax)


def showChart(stockName, item_code):

    end_time = datetime.now()
    start_time = (end_time+timedelta(days=-90)).strftime('%Y-%m-%d')

    df = yf.download(tickers = (item_code +'.KQ'), start=start_time, end=end_time.strftime('%Y-%m-%d'))
    if df.empty : 
        df = yf.download(tickers = (item_code +'.KS'), start=start_time, end=end_time.strftime('%Y-%m-%d'))

    ax,axv,ax2 = fplt.create_plot('CHART', rows=3)
    ax.set_visible(xgrid=True, ygrid=True)

    # price chart
    plot_heikin_ashi(df, ax)
    # plot_bollinger_bands(df, ax)
    # plot_ema(df, ax)

    # volume chart
    plot_heikin_ashi_volume(df, axv)
    # plot_vma(df, ax=axv)

    # some more charts
    # plot_accumulation_distribution(df, ax2)
    # plot_on_balance_volume(df, ax3)
    plot_rsi(df, ax2)

    # restore view (X-position and zoom) when we run this example again
    fplt.autoviewrestore()

    fplt.show()