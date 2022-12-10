import panel as pn
import holoviews as hv
import stumpy
import numpy as np , pandas as pd
import os
import yfinance as yf
import param , hvplot.pandas
pn.extension()

def getDF(ticker ,timeframe='1d'):
    df = yf.Ticker(ticker).history(interval=timeframe,start="2010-01-01" , end="2022-12-01")
    return df

def hvplot(avg, highlight):
    return avg.hvplot(height=500 , width=1000 , grid=True) * highlight.hvplot.scatter(color='orange', padding=0.1)

def find_outliers(ticker='MSFT' , variable='Close', window=30, sigma=10, view_fn=hvplot):
    data = getDF(ticker)
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = (np.abs(residual) > std * sigma)
    return hvplot(avg, avg[outliers])

def create_app():
    select = pn.widgets.Select(name='Select Ticker', options=['MSFT', 'AMZN', 'TSLA' ,'OXY'])
    window = pn.widgets.IntSlider(name='window', value=30, start=1, end=60)
    sigma = pn.widgets.IntSlider(name='sigma', value=3, start=0, end=20)
    interactive = pn.bind(find_outliers, ticker=select , window=window, sigma=sigma)
    return pn.Column('# Outlier Detection - US Market',select,window, sigma, interactive)


def find_patterns(ticker1='MSFT' , ticker2='TSLA' , timeframe='1d' , variable='Close', view_fn=hvplot):
    DF1 = getDF(ticker1,timeframe); DF2 = getDF(ticker2,timeframe)
    m=200
    mp = stumpy.stump(T_A = DF1['Close'], m = m, T_B = DF2['Close'], ignore_trivial = False)
    return hvplot(avg, avg[outliers])

def create_app2():
    select = pn.widgets.Select(name='Select Main Ticker', options=['MSFT', 'AMZN', 'TSLA' ,'OXY'])
    select2 = pn.widgets.Select(name='Select Secondary Ticker', options=['MSFT', 'AMZN', 'TSLA' ,'OXY'])
    timeframe = pn.widgets.Select(name='Select Time Frame' , options=['5m','15m','30m','1h','4h','1d'])
    interactive2 = pn.bind(find_outliers, ticker1=select , ticker2=select ,timeframe = timeframe)
    return pn.Column('# Similar Pattern Detection - US Market',select,select2,timeframe , interactive2)

def main():
    APP_ROUTES = {"/app1": create_app, "app2": pn.pane.Markdown("# App2")}
    pn.serve(APP_ROUTES, port=5006 ,  autoreload = True ) #, allow_websocket_origin=["127.0.0.1:5006"], address="127.0.0.1", show=False)
    return

if __name__ == '__main__':
     main()

