import panel as pn
import holoviews as hv

import numpy as np , pandas as pd
import os
import yfinance as yf
import param , hvplot.pandas
pn.extension()

def getDF(ticker):
    df = yf.Ticker(ticker).history(interval='1d',start="2010-01-01" , end="2022-12-01")
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
    select = pn.widgets.Select(name='Select Ticker', options=['MSFT', 'AMZN', 'TSLA'])
    window = pn.widgets.IntSlider(name='window', value=30, start=1, end=60)
    sigma = pn.widgets.IntSlider(name='sigma', value=3, start=0, end=20)
    interactive = pn.bind(find_outliers, ticker=select , window=window, sigma=sigma)
    return pn.Column('# Outlier Detection - US Market',select,window, sigma, interactive)

def main():
    APP_ROUTES = {"/app1": create_app, "app2": pn.pane.Markdown("# App2")}
    pn.serve(APP_ROUTES, port=5006 ,  autoreload = True ) #, allow_websocket_origin=["127.0.0.1:5006"], address="127.0.0.1", show=False)
    return

if __name__ == '__main__':
     main()

