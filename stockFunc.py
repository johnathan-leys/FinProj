# This file contains some basic functions to be performed on stock data

import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import os

# If you clone this repo, be sure to update the location of your own API key
with open(".APIkeys", 'r') as file:
    API_KEY = file.readline().strip().split()[0]

ALPHA_URL = 'https://www.alphavantage.co/query'

def get_stock_data(symbol, interval='1min'):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY
    }
    response = requests.get(ALPHA_URL, params=params)
    data = response.json()
    return data['Time Series ({})'.format(interval)]

def plot_prices(data):      # Basic Matplotlib plot
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index)
    df['4. close'] = df['4. close'].astype(float)
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['4. close'])
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.title('Stock Price: ' + stock_symbol)
    plt.grid(True)
    plt.show()
   
def plot_mplfinance(data, stock_symbol, chart_type='candle', **kwargs): # Enhanced mplfinance plot
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index)
    df['Open'] = df['1. open'].astype(float)
    df['High'] = df['2. high'].astype(float)
    df['Low'] = df['3. low'].astype(float)
    df['Close'] = df['4. close'].astype(float)
    df['Volume'] = df['5. volume'].astype(float)

    # Create the plot with additional customization options
    mpf.plot(df, type=chart_type, title=f'{stock_symbol} {chart_type.capitalize()} Chart',
             ylabel='Price', datetime_format='%H:%M', xrotation=45, **kwargs)
    
def calculate_volatility(data, window=15):
    df = pd.DataFrame.from_dict(data, orient='index')
    df.index = pd.to_datetime(df.index)
    df['Close'] = df['4. close'].astype(float)
    
    # Calculate daily returns
    df['Returns'] = df['Close'].pct_change()

    # Calculate rolling volatility (standard deviation of daily returns)
    df['Volatility'] = df['Returns'].rolling(window=window).std() * np.sqrt(window)
    
    return df[['Close', 'Volatility']]




if __name__ == '__main__':
    stock_symbol = 'TSLA'  # Test stock symbol
    interval = '1min'  # Options are: '5min', '15min', '30min', or '60min'
    
    stock_data = get_stock_data(stock_symbol, interval)
    plot_prices(stock_data)
    plot_mplfinance(stock_data, 'candle', style='nightclouds', mav=(5, 20), volume=True)

    if not os.path.exists('DataFiles'):
        os.makedirs('DataFiles')
    calculate_volatility(stock_data).to_csv('DataFiles/' + stock_symbol + 'Volatility.csv')
    
