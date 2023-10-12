#   This file contains more complex trading strategies than the simple ones built into the StockData class.
# The ta.Strategy obj is used.

from StockObj import *

import pandas_ta as ta

#   Define strategies here:
All_Strategy = ta.AllStrategy   # Requires TA-Lib

CustomStrategy = ta.Strategy(   # Example from pandas-ta README
    name="Momo and Volatility",
    description="SMA 30,75, BBANDS, RSI, MACD and Volume SMA 20",
    ta=[
        {"kind": "sma", "length": 30},
        {"kind": "sma", "length": 99},
        {"kind": "bbands", "length": 20},
        {"kind": "rsi"},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOLUME"},
    ]
)

obv_vwma50_strat = ta.Strategy(
    name="OBV, VWMA",
    description="On balance volume and volume-weighted moving average",
    ta = [
            {"kind": "obv"},
            {"kind": "vwma", "length":50, "prefix": "VWMA_{}".format(50)}
        ]
)

log_return = ta.Strategy(      #   find log return with pandas_ta
    name="Log Return",
    description="Log return using pandas_ta",
    ta = [
            {"kind": "log_return", "close": "Close", "cumulative": False, "append": True}
        ]
)

atr_kc_macd = ta.Strategy(      #   Examine volatility with ATR, KC. Combine with mavg convergence.
    name="ATR, KC, and MACD",
    description="Custom strategy with ATR, Keltner Channels, and MACD indicators",
    ta=[
        {"kind": "atr", "length": 14},
        {"kind": "kc", "length": 20, "mult": 2.0},
        {"kind": "macd", "fast": 12, "slow": 26, "signal": 9}
    ]
)

cycle_indicators = ta.Strategy(
    name="Cycle Indicators",
    description="Custom strategy with Cycle Indicators: Schaff trend cycle, Fisher transform L9, Triple Exp MAg",
    ta=[
        {"kind": "stc", "length": 14, "cycle_length": 10, "smooth1": 3, "smooth2": 3},
        {"kind": "fisher", "length": 9},
        {"kind": "trix", "length": 15}
    ]
)



if __name__ == '__main__':

    # If you clone this repo, be sure to update the location of your own API key
    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    stock_symbol = 'NVDA'  
    NVDA = StockData(API_KEY, stock_symbol)
    NVDA.fetch_stock_data()

    print(NVDA.data)
    NVDA.execute_strategy(log_return)
    NVDA.execute_strategy(obv_vwma50_strat)
    NVDA.execute_strategy(CustomStrategy)
    NVDA.execute_strategy(atr_kc_macd)
    NVDA.execute_strategy(cycle_indicators)
    NVDA.df_to_csv()
    print(NVDA.data)


    
