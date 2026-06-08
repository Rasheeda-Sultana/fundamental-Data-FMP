#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#pip install polygon-api-client

# import modules
from polygon import RESTClient
import pandas as pd

# api key from config
from polygonAPIkey import polygonAPIkey
# OR just assign your API as a string variable
# polygonAPIkey = 'apiKeyGoesHere'

# create client and authenticate w/ API key
client = RESTClient(polygonAPIkey) # api_key is used

tickers = []
for t in client.list_tickers(market="stocks", type="CS", active=True , limit=1000):
    tickers.append(t.ticker)
print(tickers)
        
# final ticker list
sorted_tickers = sorted(tickers)

pd.DataFrame(sorted_tickers[:50], columns=['symbol']).to_csv('symbol_list.csv', index=False)