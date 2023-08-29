#   This file contains more complex trading strategies than the simple ones built into the StockData
#   class. The strategies typically still modify the data in the base StockData class

from StockObj import *

import pandas_ta as ta

#   Define strategies here:
AllStrategy = ta.AllStrategy

#   Might not even want this class, can add function to base and just include the strategies file
#   ---------------------------------------------------------------------------------------------

class Strategies(StockData):
    
    def execute_strategy(self, strategy = ta.CommonStrategy):
        self.data.ta.strategy(strategy)

if __name__ == '__main__':
    # If you clone this repo, be sure to update the location of your own API key
    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    stock_symbol = 'NVDA'  
    NVDA = Strategies(API_KEY, stock_symbol)
    NVDA.fetch_stock_data()
    NVDA.execute_strategy()

    print(NVDA.data)


    
