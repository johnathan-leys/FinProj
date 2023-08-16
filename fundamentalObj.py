#   This file contains basic company fundamental information/functions from the AlphaVantage API 

import requests
import mplfinance as mpf
import os

class CompFundamentals:

    ALPHA_URL = 'https://www.alphavantage.co/query'
      
    def __init__(self, symbol, api_key):
        self.symbol = symbol
        self.api_key = api_key
        self.fundamentals = None

    def fetch_fundamental_data(self):
        params = {
            'function': 'OVERVIEW',
            'symbol': self.symbol,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()

        self.fundamentals = jdata if isinstance(jdata, dict) else None
        return self.fundamentals
    

if __name__ == '__main__':

    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    company_symbol = 'J'
    
    fund_test = CompFundamentals(company_symbol, API_KEY)
    fund_test.fetch_fundamental_data()

    if fund_test.fundamentals is not None:
        print("Company Fundamentals:")
        print(fund_test.fundamentals)
    else:
        print("Fundamentals not available.")