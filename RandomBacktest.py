# Working on backtest implementation, starting with this random backtest.

from StockObj import StockData
import random

def backtest_custom_strategy(stock_symbol, api_key):
    # Initialize
    stock_data = StockData(api_key, stock_symbol)
    stock_data.fetch_stock_data()
    
    # Generate random signals using pythons random
    stock_data.data['Random_Signal'] = [random.choice(['buy', 'sell', 'hold']) for _ in range(len(stock_data.data))]
    stock_data.data['Buy_Signal'] = stock_data.data['Random_Signal'] == 'buy'
    stock_data.data['Sell_Signal'] = stock_data.data['Random_Signal'] == 'sell'
    

    # Backtest execution, no trans costs, dump everything we can per trade. Should get profit every time! /s
    initial_balance = 100000  # $100k
    balance = initial_balance
    position = 0
    for idx, row in stock_data.data.iterrows():     # Dont need index, but had some trouble with iter

        if row['Buy_Signal'] and balance > row['Close']:
            position = balance // row['Close']
            balance -= position * row['Close']
        elif row['Sell_Signal'] and position > 0:
            balance += position * row['Close']
            position = 0
    
    # Final Portfolio Value
    final_portfolio_value = balance + (position * stock_data.data['Close'].iloc[-1])
    total_return = (final_portfolio_value - initial_balance) / initial_balance
    
    # Print results
    print(f"Initial Balance: ${initial_balance}")
    print(f"Final Portfolio Value: ${final_portfolio_value}")
    print(f"Total Return of Random Signals: {total_return * 100:.2f}%")

    return stock_data.data

if __name__ == '__main__':
    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    backtest_custom_strategy('AAPL', API_KEY)
