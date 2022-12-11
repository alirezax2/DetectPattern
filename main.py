import panel as pn
import holoviews as hv
from holoviews import opts
import stumpy
import numpy as np , pandas as pd
import os
import yfinance as yf
import param , hvplot.pandas
pn.extension()
hv.extension('bokeh')

def getDF(ticker ,timeframe='1d'):
    df = yf.Ticker(ticker).history(interval=timeframe,start="2010-01-01" , end="2022-12-01")
    return df

def myhvplot(avg, highlight):
    return avg.hvplot(height=500 , width=1000 , grid=True) * highlight.hvplot.scatter(color='orange', padding=0.1)

def find_outliers(ticker='MSFT' , variable='Close', window=30, sigma=10, view_fn=hvplot):
    data = getDF(ticker)
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = (np.abs(residual) > std * sigma)
    return myhvplot(avg, avg[outliers])

def create_app():
    select = pn.widgets.Select(name='Select Ticker', options=['MSFT', 'AMZN', 'TSLA' ,'OXY'])
    window = pn.widgets.IntSlider(name='window', value=30, start=1, end=60)
    sigma = pn.widgets.IntSlider(name='sigma', value=3, start=0, end=20)
    interactive = pn.bind(find_outliers, ticker=select , window=window, sigma=sigma)
    return pn.Column('# Outlier Detection - US Market',select,window, sigma, interactive)


def find_patterns(ticker1='MSFT' , ticker2='TSLA' , timeframe='1d' , variable='Close', view_fn=hvplot):
    DF1 = getDF(ticker1,timeframe); DF2 = getDF(ticker2,timeframe)
    DF1 = DF1.resample('5D').mean(); DF1['Date'] = DF1.index
    DF2 = DF2.resample('5D').mean(); DF2['Date'] = DF2.index
    m=200
    mp = stumpy.stump(T_A = DF1['Close'], m = m, T_B = DF2['Close'], ignore_trivial = False)
    ticker1_motif_index = mp[:, 0].argmin()
    ticker2_motif_index = mp[ticker1_motif_index, 1]
    print(DF1.iloc[ticker1_motif_index : ticker1_motif_index + m ]['Close'])
    return hv.Curve(DF1.Close)*hv.Curve(DF1.iloc[ticker1_motif_index : ticker1_motif_index + m]['Close']).relabel(f'{ticker1}').opts( height=500 , width=500 )  + hv.Curve(DF2.Close)*hv.Curve(DF2.iloc[ticker2_motif_index : ticker2_motif_index + m]['Close']).relabel(f'{ticker2}').opts( height=500 , width=500) 

def create_app2():
    select = pn.widgets.Select(name='Select Main Ticker', options=['MSFT', 'AMZN', 'TSLA' ,'OXY'])
    select2 = pn.widgets.Select(name='Select Secondary Ticker', options=['AMZN', 'MSFT',  'TSLA' ,'OXY'])
    timeframe = pn.widgets.Select(name='Select Time Frame' , options=['1d','5m','15m','30m','1h'])
    interactive2 = pn.bind(find_patterns, ticker1=select , ticker2=select2 ,timeframe = timeframe)
    return pn.Column('# Similar Pattern Detection - US Market',select,select2,timeframe , interactive2)

def main():
    APP_ROUTES = {"/app1": create_app, "app2":create_app2 , "app3": pn.pane.Markdown("# App2")}
    pn.serve(APP_ROUTES, port=5006 ,  autoreload = True ) #, allow_websocket_origin=["127.0.0.1:5006"], address="127.0.0.1", show=False)
    return

if __name__ == '__main__':
     main()

