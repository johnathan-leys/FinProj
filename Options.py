# Yahoo_fin seems to be best Free options API
import yahoo_fin.options as ops
import pandas as pd

class OptionsData:
    def __init__(self, symbol):
        self.symbol = symbol
        self.expiry_dates = []      # Empty list
        self.options_chain = {}     # Empty dict

    def fetch_expiry_dates(self):   # Basic function to get the expiration dates for ticker
        self.expiry_dates = ops.get_expiration_dates(self.symbol)



if __name__ == '__main__':
    symbol = 'AAPL'
    options_data = OptionsData(symbol)
    
    options_data.fetch_expiry_dates()
    print(options_data.expiry_dates)

