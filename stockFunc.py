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
    data =  data['Time Series ({})'.format(interval)]
    df_data = pd.DataFrame.from_dict(data, orient='index')
    df_data.index = pd.to_datetime(df_data.index)
    return df_data

def plot_prices(data_df):      # Basic Matplotlib plot
    data_df['4. close'] = data_df['4. close'].astype(float)
    plt.figure(figsize=(12, 6))
    plt.plot(data_df.index, data_df['4. close'])
    plt.xlabel('Time')
    plt.ylabel('Stock Price')
    plt.title('Stock Price: ' + stock_symbol)
    plt.grid(True)
    plt.show()
   
def plot_mplfinance(data_df, stock_symbol, chart_type='candle', **kwargs): # Enhanced mplfinance plot
    data_df['Open'] = data_df['1. open'].astype(float)
    data_df['High'] = data_df['2. high'].astype(float)
    data_df['Low'] = data_df['3. low'].astype(float)
    data_df['Close'] = data_df['4. close'].astype(float)
    data_df['Volume'] = data_df['5. volume'].astype(float)

    # Create the plot with additional customization options
    mpf.plot(data_df, type=chart_type, title=f'{stock_symbol} {chart_type.capitalize()} Chart',
             ylabel='Price', datetime_format='%H:%M', xrotation=45, **kwargs)

# Calculates volatility 
# Inputs: dataframe, size of window to analyze, bool to include all original columns in return
def calculate_volatility(data_df, window= 15, include_all=False):
    data_df['Close'] = data_df['4. close'].astype(float)
    
    # Calculate daily returns
    data_df['Returns'] = data_df['Close'].pct_change()

    # Calculate rolling volatility (standard deviation of daily returns)
    data_df['Volatility'] =data_df['Returns'].rolling(window=window).std() * np.sqrt(window)

    if include_all:
        return data_df
    else:
        return data_df[['Close', 'Volatility']]

# Adds RSI field to input dataframe
def calculate_rsi(data_df, window=10, include_all=False):
    data_df['Close'] = data_df['4. close'].astype(float)

    # Calculate daily returns and gains/losses
    data_df['Returns'] = data_df['Close'].diff()
    data_df['Gains'] = np.where(data_df['Returns'] > 0, data_df['Returns'], 0)
    data_df['Losses'] = np.where(data_df['Returns'] < 0, abs(data_df['Returns']), 0)

    # Calculate average gains and losses using window period
    avg_gains = data_df['Gains'].rolling(window=window).mean()
    avg_losses = data_df['Losses'].rolling(window=window).mean()

    # Calculate RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    data_df['RSI'] = rsi
    if include_all:
        return data_df
    else:
        return data_df[['Close', 'RSI']]

def df_to_csv(data_df, stock_symbol, filename='AllData.csv'):
    if(filename == 'AllData.csv'):
        data_df.to_csv('DataFiles/' + stock_symbol + 'AllData.csv')
    else:
         data_df.to_csv('DataFiles/' + filename)
    

#Eventually combine functions into one that adds them all. Can just call them all  and combine




if __name__ == '__main__':
    stock_symbol = 'TSLA'  # Test stock symbol
    interval = '1min'  # Options are: '5min', '15min', '30min', or '60min'
    
    stock_data = get_stock_data(stock_symbol, interval)
    plot_prices(stock_data)
    plot_mplfinance(stock_data, 'candle', style='nightclouds', mav=(5, 20), volume=True)

    if not os.path.exists('DataFiles'):
        os.makedirs('DataFiles')
    calculate_volatility(stock_data).to_csv('DataFiles/' + stock_symbol + 'Volatility.csv')
    
