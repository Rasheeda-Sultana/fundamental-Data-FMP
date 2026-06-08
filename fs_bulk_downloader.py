#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pip OR conda install
#pip install polygon-api-client
#pip install plotly

#import modules
from polygon import RESTClient
import datetime as dt
import pandas as pd

#api key from config
from polygonAPIkey import polygonAPIkey
# OR just assign your API as a string variable
# polygonAPIkey = 'apiKeyGoesHere'

# create client and authenticate w/ API key // rate limit 5 requests per min
client = RESTClient(polygonAPIkey) # api_key is used

# assign symbol list
# symbol_list = ['AA', 'AAPL']
symbol_list = pd.read_csv('symbol_list.csv')

# Excel file output location
download_path = '/Users/Username/Desktop/fundamental_scan/fundamental_data/'

def flatten_data(financials_data, parent_key='financials', sep="_"):

    flattened_data = {}

    # Check if the input is an object with attributes (e.g., financials object)
    if hasattr(financials_data, '__dict__'):
        financials_data = vars(financials_data)
    
    for key, value in financials_data.items():
        # Construct the new key with parent_key
        new_key = f"{parent_key}{sep}{key}"
        
        # If value is a dictionary or object, recurse
        if isinstance(value, dict):
            flattened_data.update(flatten_data(value, new_key, sep))
        elif hasattr(value, '__dict__'):  # If value is another object
            flattened_data.update(flatten_data(vars(value), new_key, sep))
        else:
            # No more dict/objs, add the flattened key-value pair
            flattened_data[new_key] = value
        
    return flattened_data

def fs_download(symbol, download_path):
    data = []
    for stock_financials_obj in client.vx.list_stock_financials(
            ticker=symbol,
            filing_date_gt='1960-01-01'):
        
        row = {
            'symbol': symbol,
            'cik': stock_financials_obj.cik,
            'company_name': stock_financials_obj.company_name,
            'end_date': stock_financials_obj.end_date,
            'filing_date': stock_financials_obj.filing_date,
            'fiscal_period': stock_financials_obj.fiscal_period,
            'fiscal_year': stock_financials_obj.fiscal_year,
            'source_filing_file_url': stock_financials_obj.source_filing_file_url,
            'source_filing_url': stock_financials_obj.source_filing_url,
            'start_date': stock_financials_obj.start_date
        }
        
        # Add financial statement line items and values to row
        flattened_financials = flatten_data(stock_financials_obj.financials)
        row.update(flattened_financials)
        data.append(row)
        
    # To excel
    sheet = pd.DataFrame(data)
    if not sheet.empty:
        sheet.to_csv(f'{download_path}{symbol}.csv', index=False)
    else: 
        print(f'No data for {symbol}')
    return

def bulk_download(symbol_list, download_path):
    for symbol in symbol_list.symbol:
        fs_download(symbol, download_path)

if __name__ == "__main__":
    bulk_download(symbol_list, download_path)