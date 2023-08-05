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

    # Rename to work with mplf
    df_data.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)
    df_data = df_data.astype(float)

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


    # Create the plot with additional customization options
    mpf.plot(data_df, type=chart_type, title=f'{stock_symbol} {chart_type.capitalize()} Chart',
             ylabel='Price', datetime_format='%H:%M', xrotation=45, **kwargs)

# Calculates volatility 
# Inputs: dataframe, size of window to analyze, bool to include all original columns in return
def calculate_volatility(data_df, window= 15):
   
    # Calculate daily returns
    data_df['Returns'] = data_df['Close'].pct_change()

    # Calculate rolling volatility (standard deviation of daily returns)
    data_df['Volatility'] =data_df['Returns'].rolling(window=window).std() * np.sqrt(window)

    return data_df[['Close', 'Volatility']]

# Adds RSI field to input dataframe
def calculate_rsi(data_df, window=10):

    # Calculate daily returns, gains/losses
    data_df['Returns'] = data_df['Close'].diff()
    data_df['Gains'] = np.where(data_df['Returns'] > 0, data_df['Returns'], 0)
    data_df['Losses'] = np.where(data_df['Returns'] < 0, abs(data_df['Returns']), 0)

    # Calculate average gains and losses
    avg_gains = data_df['Gains'].rolling(window=window).mean()
    avg_losses = data_df['Losses'].rolling(window=window).mean()

    # Calculate RSI
    rs = avg_gains / avg_losses
    rsi = 100 - (100 / (1 + rs))
    data_df['RSI'] = rsi

    # Remove the unneeded gains/losses columns
    data_df.drop('Gains', axis=1, inplace=True)
    data_df.drop('Losses', axis=1, inplace=True)

    return data_df[['Close', 'RSI']] # Return just the neede fields

def df_to_csv(data_df, stock_symbol, filename='AllData.csv'):
    if(filename == 'AllData.csv'):
        data_df.to_csv('DataFiles/' + stock_symbol + 'AllData.csv')
    else:
         data_df.to_csv('DataFiles/' + filename)
    
# Daily Price Change Histogram. Reccomonede to use over longer periods of time, as of right now API
# can call up to 60min intervals. Plan is to incorporate daily data eventually
def daily_pcd(df_data):
    # Resample the DataFrame to daily frequency and forward-fill any missing values
    daily_dataframe = df_data.resample('D').last()

    # Calculate the daily returns using the 'Close' column
    daily_dataframe['Daily Returns'] = daily_dataframe['Close'].pct_change()

    # Plot the histogram of daily returns (including NaN values for the first entry of each day)
    plt.figure(figsize=(10, 6))
    plt.hist(daily_dataframe['Daily Returns'], bins=30, edgecolor='black')
    plt.title('Daily Price Change Distribution')
    plt.xlabel('Daily Returns')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
    
    return daily_dataframe



if __name__ == '__main__':
    stock_symbol = 'TSLA'  # Test stock symbol
    interval = '1min'  # Options are: '5min', '15min', '30min', or '60min'
    
    stock_data = get_stock_data(stock_symbol, interval)
    plot_prices(stock_data)
    plot_mplfinance(stock_data, 'candle', style='nightclouds', mav=(5, 20), volume=True)

    if not os.path.exists('DataFiles'):
        os.makedirs('DataFiles')
    calculate_volatility(stock_data).to_csv('DataFiles/' + stock_symbol + 'Volatility.csv')
    
