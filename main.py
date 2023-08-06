from stockFunc import *

stock_symbol = 'TSLA'  # Test stock symbol
interval = '1min'  # Options are: '5min', '15min', '30min', or '60min'

stock_data = get_stock_data(stock_symbol, interval)
daily_data = get_stock_data_daily(stock_symbol)

plot_mplfinance(stock_data, 'TSLA', style='nightclouds', mav=(5, 20), volume=True)

if not os.path.exists('DataFiles'):
     os.makedirs('DataFiles')
calculate_volatility(daily_data).to_csv('DataFiles/' + stock_symbol + 'Volatility.csv')
calculate_rsi(daily_data, 14).to_csv('DataFiles/' + stock_symbol + 'RSI.csv')

df_to_csv(daily_pcd(daily_data), stock_symbol, 'PCDHist.csv')

df_to_csv(stock_data, stock_symbol)
df_to_csv(daily_data, stock_symbol)




