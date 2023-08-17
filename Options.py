# Yahoo_fin seems to be best Free options API
import yahoo_fin.options as ops
import pandas as pd
import os
import json

class OptionsData:
    def __init__(self, symbol):
        self.symbol = symbol
        self.expiry_dates = []      # Empty list
        self.options_chain = {}     # Empty dict

    def fetch_expiry_dates(self):   # Basic function to get the expiration dates for ticker
        self.expiry_dates = ops.get_expiration_dates(self.symbol)

    def fetch_options_chain(self, expiry_date = None):
        # if expiry_date not in self.expiry_dates:
        #     raise ValueError("Invalid expiry date")

        chain = ops.get_options_chain(self.symbol, expiry_date)
        self.options_chain[expiry_date] = chain

    def get_calls(self, expiry_date = None):           # Return calls from options chain at given date
        if expiry_date not in self.options_chain:  
            self.fetch_options_chain(expiry_date)
        return self.options_chain[expiry_date]['calls']

    def get_puts(self, expiry_date= None):            # Return puts from options chain at given date
        if expiry_date not in self.options_chain:
            self.fetch_options_chain(expiry_date)
        return self.options_chain[expiry_date]['puts']
    
    def to_csv(self):   # Outputs Earliest expiration date options to csv  
        if not os.path.exists('DataFiles'): # Create dir to store output data if does not exist
            os.makedirs('DataFiles')

        self.get_puts().to_csv('DataFiles/' + self.symbol + 'puts.csv')
        self.get_calls().to_csv('DataFiles/' + self.symbol + 'calls.csv')
 


if __name__ == '__main__':
    symbol = 'AAPL'
    options_data = OptionsData(symbol)
    
    options_data.fetch_expiry_dates()
    print(options_data.expiry_dates)

    options_data.fetch_options_chain(options_data.expiry_dates[0])
    # print(options_data.options_chain)

    print(options_data.get_calls())


    options_data.to_csv()

   