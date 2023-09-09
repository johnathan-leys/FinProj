from StockObj import *

with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

# Testing with Daily SPY
stock_symbol = 'SPY'   
AAPL = StockData(API_KEY, stock_symbol)
AAPL.fetch_stock_data()
AAPL.plot_prices()
AAPL.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
AAPL.calculate_volatility()
AAPL.calculate_rsi()
AAPL.df_to_csv()
AAPL.daily_pcd()
AAPL.plot_bollinger_bands()
AAPL.mplf_plot_bollinger_bands()
AAPL.df_to_csv()
print(AAPL.data)

# Testing with 1min interval QQQ
stock_symbol = 'QQQ' 
interval = '1min'  
QQQ = StockData(API_KEY, stock_symbol, interval)
QQQ.fetch_stock_data()
QQQ.plot_prices()
QQQ.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
QQQ.calculate_volatility()
QQQ.calculate_rsi()
QQQ.plot_bollinger_bands()
QQQ.mplf_plot_bollinger_bands()
QQQ.df_to_csv()
QQQ.daily_pcd()




