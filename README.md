
# Fundamental Stock Data Analysis & Financial Ratio Scanner

Python scripts for retrieving, analyzing, and sorting stock fundamental data using the Financial Modeling Prep (FMP) API and the `fundamentalanalysis` Python wrapper.

This project demonstrates how to collect company profiles, financial statements, key metrics, financial ratios, growth data, analyst ratings, discounted cash flow values, and historical stock information programmatically using Python.

---

# Features

- Retrieve publicly traded company data from FMP
- Access stock listings across multiple exchanges
- Analyze financial statements and key metrics
- Fetch analyst ratings and DCF valuations
- Retrieve balance sheet, income statement, and cash flow data
- Screen and sort companies using financial ratios
- Download historical stock and dividend data
- Perform automated equity research workflows

---

# Project Structure

```bash
fundamentalDataFMP/
│
├── README.md
├── fmpSecret.py
├── getFundamentalDataFMP.py
└── fundamentalDataSortFMP.py
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/AdamGetbags/fundamentalDataFMP.git
```

Move into the project directory:

```bash
cd fundamentalDataFMP
```

Install required dependencies:

```bash
pip install pandas fundamentalanalysis
```

---

# Setup

Create a file named `fmpSecret.py` and add your Financial Modeling Prep API key:

```python
# -*- coding: utf-8 -*-
"""

Get fundamental data FMP API secrets
@author: Adam Getbags

"""

fmpSecret = 'apiKeyGoesHere'
```

Get your API key from:

https://financialmodelingprep.com/

---

# File Overview

## 1. fmpSecret.py

Stores the Financial Modeling Prep API key used for authentication.

---

## 2. getFundamentalDataFMP.py

Retrieves detailed company fundamental data including:

- Company profile
- Dividend information
- Beta values
- Analyst ratings
- Discounted cash flow (DCF)
- Enterprise value
- Financial statements
- Key metrics
- Financial ratios
- Growth metrics
- Historical stock prices
- Dividend history

### Full Code

```python
# -*- coding: utf-8 -*-
"""

Get fundamental data
@author: Adam Getbags

Data provided by Financial Modeling Prep
https://site.financialmodelingprep.com/developer/docs/

Python API wrapper by
https://github.com/JerBouma/FundamentalAnalysis

"""

# pip install fundamentalanalysis

# import modules
import pandas as pd
import fundamentalanalysis as fa
from fmpSecret import fmpSecret as api_key

ticker = "AAPL"

# show the available tickers
allTickers = fa.available_companies(api_key)

# get unique exchange names
allExchanges = allTickers.exchangeShortName.unique()
print(allExchanges)

# get all ticker data on single exchange
tickersOnExchange = allTickers[
    allTickers.exchangeShortName == 'NASDAQ'
]
print(tickersOnExchange)

# get all ticker data on multiple exchanges
tickersOnExchanges = allTickers[
    (allTickers.exchangeShortName == 'NASDAQ') |
    (allTickers.exchangeShortName == 'NYSE') |
    (allTickers.exchangeShortName == 'AMEX')
]
print(tickersOnExchanges)

# accessing the stock symbols
symbols = list(tickersOnExchanges.index)
print(symbols)

# collect general company information
profile = fa.profile(ticker, api_key)
print(profile)

# get last dividend
lastDiv = profile.loc['lastDiv'][0]
print(lastDiv)

# get beta
beta = profile.loc['beta'][0]
print(beta)

# collect recent company quotes
quotes = fa.quote(ticker, api_key)
print(quotes)

# collect market cap and enterprise value
enterprise_value = fa.enterprise(ticker, api_key)

# get specific year enterprise value
evByYear = enterprise_value['2021'].loc['enterpriseValue']

# show recommendations of analysts
ratings = fa.rating(ticker, api_key)
print(ratings)

# obtain DCFs over time
dcf_annually = fa.discounted_cash_flow(
    ticker,
    api_key,
    period="annual"
)
print(dcf_annually)

# collect the balance sheet statements
balance_sheet_annually = fa.balance_sheet_statement(
    ticker,
    api_key,
    period="annual"
)

# individual balance sheet items by year
print(list(balance_sheet_annually['2021'].index))

# collect the income statements
income_statement_annually = fa.income_statement(
    ticker,
    api_key,
    period="annual"
)

# individual income statement items by year
print(list(income_statement_annually['2021'].index))
print('- - -')
print(income_statement_annually['2021'].loc['netIncomeRatio'])

# collect the cash flow statements
cash_flow_statement_annually = fa.cash_flow_statement(
    ticker,
    api_key,
    period="annual"
)

# individual cash flow items by year
print(list(cash_flow_statement_annually['2021'].index))

# free cash flow
fcf = cash_flow_statement_annually['2021'].loc['freeCashFlow']
print(fcf)

# show key metrics
key_metrics_annually = fa.key_metrics(
    ticker,
    api_key,
    period="annual"
)
print(key_metrics_annually)

# return on invested capital
roic = key_metrics_annually['2021'].loc['roic']
print(roic)

# show financial ratios
financial_ratios_annually = fa.financial_ratios(
    ticker,
    api_key,
    period="annual"
)

print(financial_ratios_annually['2021'])

ccc = financial_ratios_annually['2021'].loc[
    'cashConversionCycle'
]
print(ccc)

# show company growth
growth_annually = fa.financial_statement_growth(
    ticker,
    api_key,
    period="annual"
)
print(growth_annually)

# download general stock data
stock_data = fa.stock_data(
    ticker,
    period="max",
    interval="1d"
)

# download detailed stock data
stock_data_detailed = fa.stock_data_detailed(
    ticker,
    api_key,
    begin="2000-01-01",
    end="2020-01-01"
)
print(stock_data_detailed.columns)

# download dividend history
dividends = fa.stock_dividend(
    ticker,
    api_key,
    begin="2000-01-01",
    end="2020-01-01"
)
print(dividends.adjDividend)
```

---

## 3. fundamentalDataSortFMP.py

Screens and sorts companies based on financial ratios.

Current implementation:

- Retrieves NASDAQ-listed stocks
- Collects annual net profit margin data
- Stores results in a Pandas DataFrame
- Sorts companies by profitability
- Displays top-performing companies

### Full Code

```python
# -*- coding: utf-8 -*-
"""

Get fundamental data sorting
@author: Adam Getbags

Data provided by Financial Modeling Prep
https://site.financialmodelingprep.com/developer/docs/

Python API wrapper by
https://github.com/JerBouma/FundamentalAnalysis

"""

# import modules
import pandas as pd
import fundamentalanalysis as fa
from fmpSecret import fmpSecret as api_key

# empty data structure
bulkData = pd.DataFrame(
    columns=['symbol', 'npmData']
)

# show the available tickers
allTickers = fa.available_companies(api_key)

# get unique exchange names
allExchanges = allTickers.exchangeShortName.unique()
print(allExchanges)

# get all ticker data on single exchange
companiesOnExchange = allTickers[
    (allTickers.exchangeShortName == 'NASDAQ') &
    (allTickers.type == 'stock')
]
print(companiesOnExchange[:25])

# accessing the stock symbols
symbols = list(companiesOnExchange[:25].index)
print(symbols)

# for each symbol in list
for i in symbols:

    # request most recent npm data
    financial_ratios_annually = fa.financial_ratios(
        i,
        api_key,
        period="annual"
    )

    # get net profit margin data
    npmData = financial_ratios_annually[
        financial_ratios_annually.columns[0]
    ].loc['netProfitMargin']

    # save to DataFrame
    bulkData.loc[len(bulkData)] = [i, npmData]

# sort DataFrame
bulkData = bulkData.sort_values(
    'npmData',
    ascending=False,
    ignore_index=True
)

# get top 10 companies by net profit margin
bulkData.head(10)
```

---

# Example Financial Metrics

The project can analyze:

- Net Profit Margin
- Return on Invested Capital (ROIC)
- Cash Conversion Cycle (CCC)
- Free Cash Flow
- Enterprise Value
- Revenue Growth
- Earnings Growth
- Dividend Data
- Market Capitalization
- Historical Price Data

---

# Example Usage

Run the main fundamental data script:

```bash
python getFundamentalDataFMP.py
```

Run the financial ratio sorting script:

```bash
python fundamentalDataSortFMP.py
```

---

# Data Sources

Financial data provided by:

- Financial Modeling Prep API  
  https://site.financialmodelingprep.com/developer/docs/

Python wrapper used:

- FundamentalAnalysis  
  https://github.com/JerBouma/FundamentalAnalysis

---

# Future Improvements

- Export results to CSV or Excel
- Add visualization dashboards
- Include technical indicators
- Add multi-factor stock screening
- Add portfolio analysis tools
- Add backtesting functionality

---

# Disclaimer

This project is intended for educational and research purposes only.

It does not constitute financial advice, investment recommendations, or trading guidance.




README and GitHub documentation adapted for project presentation.
````
