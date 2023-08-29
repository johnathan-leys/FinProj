#   This file contains the StockData class with custom functions for fetching and analyzing
#   stock data, stored in self.data.  

import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import os

class StockData:
    ALPHA_URL = 'https://www.alphavantage.co/query'

    def __init__(self, api_key, symbol='SPY', interval='Daily'):
        self.symbol = symbol                # Stock Ticker
        self.api_key = api_key              # API key
        self.data = pd.DataFrame()          # Dataframe containing stock history
        self.interval = interval            # Interval, 1-60min Intraday or Daily
        self.metadata = None

    def fetch_stock_data(self):

        if(self.interval == 'Daily'):       # Different calls for daily vs intraday
            params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.symbol,
            'apikey': self.api_key
        }
        else:
            params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': self.symbol,
            'interval': self.interval,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()
        self.metadata = jdata.get('Meta Data', {})                  # Strip metadata from json
        jdata =  jdata['Time Series ({})'.format(self.interval)]
        self.data = pd.DataFrame.from_dict(jdata, orient='index')   # Convert financial data to dataframe
        self.data.index = pd.to_datetime(self.data.index)

        # Rename to work with mplf
        self.data.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. volume': 'Volume'}, inplace=True)
        self.data = self.data.astype(float)

    def plot_prices(self):    # Basic Matplotlib plot
        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index, self.data['Close'])
        plt.xlabel('Time')
        plt.ylabel('Stock Price')
        plt.title('Stock Price: ' + self.symbol)
        plt.grid(True)
        plt.show()

    def plot_mplfinance(self, chart_type='candle', **kwargs): # Enhanced mplfinance plot
        # Create the plot with additional customization options
        mpf.plot(self.data, type=chart_type, title=f'{self.symbol} {chart_type.capitalize()} Chart',
             ylabel='Price',  xrotation=45, **kwargs)

    def calculate_volatility(self, window= 15):
        # Calculate returns
        self.data['ReturnsPct'] = self.data['Close'].pct_change()

        # Calculate volatility
        self.data['Volatility'] = self.data['ReturnsPct'].rolling(window=window).std() * np.sqrt(window)

        return self.data[['Close', 'Volatility']]  # Return just the needed columns

    # Calculate and add RSI field to data
    def calculate_rsi(self, window=10):
        # Calculate daily returns, gains/losses
        self.data['Returns'] = self.data['Close'].diff()
        self.data['Gains'] = np.where(self.data['Returns'] > 0, self.data['Returns'], 0)
        self.data['Losses'] = np.where(self.data['Returns'] < 0, abs(self.data['Returns']), 0)

        # Calculate average gains and losses
        avg_gains = self.data['Gains'].rolling(window=window).mean()
        avg_losses = self.data['Losses'].rolling(window=window).mean()

        # Calculate RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        self.data['RSI'] = rsi

        # Remove the unneeded gains/losses columns
        self.data.drop('Gains', axis=1, inplace=True)
        self.data.drop('Losses', axis=1, inplace=True)

        return self.data[['Close', 'RSI']] # Return just the RSI fields
    
    # Plots a histogram of Daily Price Change Distribution
    def daily_pcd(self):
        # Resample the DataFrame to daily if it is not already
        daily_dataframe = self.data.resample('D').last()
        # Ensure more than one date is provided
        if(len(daily_dataframe) <= 1):              
            print('Not enough dates in data provided, check your interval')
            return

        # Calculate the daily returns using the 'Close' column
        daily_dataframe['Daily Returns'] = daily_dataframe['Close'].pct_change()

        # Plot the histogram of daily returns
        plt.figure(figsize=(10, 6))
        plt.hist(daily_dataframe['Daily Returns'], bins=30, edgecolor='black')
        plt.title('Daily Price Change Distribution: ' + self.symbol)
        plt.xlabel('Daily Returns')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()
        
        return daily_dataframe
    
    def calculate_bollinger_bands(self, window=20, num_std=2):
        # Moving average
        self.data['Move_avg'] = self.data['Close'].rolling(window=window).mean()

        # Standard deviation
        self.data['Std_dev'] = self.data['Close'].rolling(window=window).std()

        # Upper and lower Bollinger Bands
        self.data['BB_up'] = self.data['Move_avg'] + (num_std * self.data['Std_dev'])
        self.data['BB_low'] = self.data['Move_avg'] - (num_std * self.data['Std_dev'])

        return self.data[['BB_up', 'BB_low']]   #Return the new entries
    
    def plot_bollinger_bands(self, window=20, num_std=2):   # Basic Bollinger band plot with mpl
        self.calculate_bollinger_bands(window, num_std)     # Add the needed BB entries if not there yet
        #   Plot the new Bollinger bands
        plt.figure(figsize=(10, 6))
        plt.plot(self.data.index, self.data['Close'], label='Close Price', color='blue')
        plt.plot(self.data.index, self.data['Move_avg'], label='Moving Average', color='orange')
        plt.plot(self.data.index, self.data['BB_up'], label='Upper Bollinger Band', color='green', linestyle='dashed')
        plt.plot(self.data.index, self.data['BB_low'], label='Lower Bollinger Band', color='red', linestyle='dashed')
        plt.fill_between(self.data.index, self.data['BB_up'], self.data['BB_low'], color='lightgray', alpha=0.5)
    
        plt.title('Bollinger Bands')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()

    def mplf_plot_bollinger_bands(self, window=20, num_std=2, **kwargs):
        self.calculate_bollinger_bands(window, num_std)                 # Add the needed BB entries if not there yet

        add_plot = mpf.make_addplot(self.data[['BB_up', 'BB_low']])     # Forces mplf to recognize BB entries

        self.plot_mplfinance(addplot=add_plot, **kwargs)                # Use our owm mplf function that passes in new data

    def df_to_csv(self, filename='AllData.csv'):
        if not os.path.exists('DataFiles'): # Create dir to store output data if does not exist
            os.makedirs('DataFiles')

        if(filename == 'AllData.csv'):
            self.data.to_csv('DataFiles/' + self.symbol + 'AllData.csv')
        else:
            self.data.to_csv('DataFiles/' + filename)
    
    

if __name__ == '__main__':
    # If you clone this repo, be sure to update the location of your own API key
    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    stock_symbol = 'SPY'  
    
    SPY = StockData(API_KEY, stock_symbol)
    SPY.fetch_stock_data()
   
    SPY.plot_prices()
    SPY.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
    SPY.calculate_volatility()
    SPY.calculate_rsi()

    SPY.daily_pcd()

    SPY.df_to_csv()

    

    print(SPY.data)



   