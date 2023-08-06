import requests
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
import os

class StockData:
    ALPHA_URL = 'https://www.alphavantage.co/query'

    def __init__(self, api_key, symbol='SPY', interval='Daily'):
        self.symbol = symbol        # Stock Ticker
        self.api_key = api_key      # API key
        self.data = None            # Dataframe containing stock history
        self.interval = interval            # Interval, 1-60min Intradat or Daily

    def get_stock_data(self):

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
        jdata =  jdata['Time Series ({})'.format(self.interval)]
        self.data = pd.DataFrame.from_dict(jdata, orient='index')
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
             ylabel='Price', datetime_format='%H:%M', xrotation=45, **kwargs)

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

    def df_to_csv(self, filename='AllData.csv'):
        if(filename == 'AllData.csv'):
            self.data.to_csv('DataFiles/' + self.symbol + 'AllData.csv')
        else:
            self.data.to_csv('DataFiles/' + filename)


if __name__ == '__main__':
    # If you clone this repo, be sure to update the location of your own API key
    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    stock_symbol = 'AAPL'  
    
    Apple_Obj = StockData(API_KEY, stock_symbol)
    Apple_Obj.get_stock_data()
   
    Apple_Obj.plot_prices()
    Apple_Obj.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
    Apple_Obj.calculate_volatility()
    Apple_Obj.calculate_rsi()

    Apple_Obj.df_to_csv()

    print(Apple_Obj.data)



   