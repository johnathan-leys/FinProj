import requests
import pandas as pd
import matplotlib.pyplot as plt

# If you clone this repo, be sure to update the location of your own API key

with open(".APIkeys", 'r') as file:
    API_KEY = file.readline().strip().split()[0]

BASE_URL = 'https://www.alphavantage.co/query'

def get_stock_data(symbol, interval='1min'):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return data['Time Series ({})'.format(interval)]

def plot_stock_prices(data):
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

if __name__ == '__main__':
    stock_symbol = 'TSLA'  # Test stock symbol
    interval = '1min'  # Options are: '5min', '15min', '30min', or '60min'
    
    stock_data = get_stock_data(stock_symbol, interval)
    plot_stock_prices(stock_data)
    
