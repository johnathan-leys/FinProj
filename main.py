from StockObj import *

with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

# Testing with Daily SPY
stock_symbol = 'SPY'   
SPY = StockData(API_KEY, stock_symbol)
SPY.get_stock_data()
SPY.plot_prices()
SPY.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
SPY.calculate_volatility()
SPY.calculate_rsi()
SPY.df_to_csv()
SPY.daily_pcd()

# Testing with 1min interval QQQ
stock_symbol = 'QQQ' 
interval = '1min'  
QQQ = StockData(API_KEY, stock_symbol, interval)
QQQ.get_stock_data()
QQQ.plot_prices()
QQQ.plot_mplfinance(style='nightclouds', mav=(5, 20), volume=True)
QQQ.calculate_volatility()
QQQ.calculate_rsi()
QQQ.df_to_csv()
QQQ.daily_pcd()




