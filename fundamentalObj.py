#   This file contains basic company fundamental information/functions from the AlphaVantage API 

import requests
import mplfinance as mpf
import os

class CompFundamentals:

    ALPHA_URL = 'https://www.alphavantage.co/query'
      
    def __init__(self, symbol, api_key):
        self.symbol = symbol
        self.api_key = api_key
        self.overview = None
        self.income_statement = None
        self.balance_sheet = None
        self.cash_flow = None

    def fetch_fundamental_data(self):
        params = {
            'function': 'OVERVIEW',
            'symbol': self.symbol,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()

        self.overview = jdata if isinstance(jdata, dict) else None
        return self.overview
    
    def fetch_income_statement(self):
        params = {
            'function': 'INCOME_STATEMENT',
            'symbol': self.symbol,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()

        self.income_statement = jdata if isinstance(jdata, dict) else None
        return self.income_statement
    
    def fetch_balance_sheet(self):
        params = {
            'function': 'BALANCE_SHEET',
            'symbol': self.symbol,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()

        self.balance_sheet = jdata if isinstance(jdata, dict) else None
        return self.balance_sheet
    

    #   Cash flow is normalized, mapped to GAAP and IFRS taxonomies of the SEC from AlphaVantage. Some
    #   fields may be implied...
    def fetch_cash_flow(self):
        params = {
            'function': 'CASH_FLOW',
            'symbol': self.symbol,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()

        self.cash_flow = jdata if isinstance(jdata, dict) else None
        return self.balance_sheet
    
    def fetch_eps(self):
        params = {
            'function': 'EARNINGS',
            'symbol': self.symbol,
            'apikey': self.api_key
        }

        response = requests.get(self.ALPHA_URL, params=params)
        jdata = response.json()

        self.earnings = jdata if isinstance(jdata, dict) else None
        return self.earnings
    
  
    

if __name__ == '__main__':

    with open(".APIkeys", 'r') as file:
        API_KEY = file.readline().strip().split()[0]

    company_symbol = 'AAPL'
    
    fund_test = CompFundamentals(company_symbol, API_KEY)
    fund_test.fetch_fundamental_data()
    print('-------Fundamentals-----------------------')
    print(fund_test.overview)
    print('------------------------------------------')

    print('-------Income Statement--------------------------')
    fund_test.fetch_income_statement()
    print(fund_test.income_statement['annualReports'][0])  # Print most recent annual report
    print('------------------------------------------')

    print('-------Balance Sheet----------------------')
    fund_test.fetch_balance_sheet()
    print(fund_test.balance_sheet['annualReports'][0])   # Print most recent balance sheet
    print('------------------------------------------')

    print('-------Cash Flow--------------------------')
    fund_test.fetch_cash_flow()
    print(fund_test.cash_flow['annualReports'][0])
    print('------------------------------------------')

    print('-------Earnings--------------------------')
    fund_test.fetch_eps()
    print(fund_test.earnings['annualEarnings'][0])
