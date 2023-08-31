#   This file contains more complex trading strategies than the simple ones built into the StockData
#   class. The strategies typically still modify the data in the base StockData class.

from StockObj import *

import pandas_ta as ta

#   Define strategies here:
All_Strategy = ta.AllStrategy   # Requires TA-Lib

CustomStrategy = ta.Strategy(   # Example from pandas-ta README
    name="Momo and Volatility",
    description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
    ta=[
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 200},
        {"kind": "bbands", "length": 20},
        {"kind": "rsi"},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
    ]
)

obv_vwma50_strat = ta.Strategy(   # 
    name="OBV, VWMA",
    description="On balance volume and volume-weighted moving average",
    ta = [
            {"kind": "obv"},
            {"kind": "vwma", "length":50, "prefix": "VWMA_{}".format(50)}
        ]
)


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

    print(NVDA.data)
    NVDA.execute_strategy(obv_vwma50_strat)
    NVDA.execute_strategy(CustomStrategy)

    print(NVDA.data)


    
