
# polygonFundamentalScanner

Fundamental Analysis Scanner in Python using the Polygon.io API.

This project automates financial statement data extraction, fundamental ratio analysis, stock screening, and CSV-based benchmarking workflows using Polygon.io financial data and Python.

---

## Repository Structure

```bash
polygonFundamentalScanner/
│
├── fs_bulk_downloader.py
├── fs_scanner.py
├── fs_ticker_list.py
└── polygonAPIkey.py
```

---

## Overview

The project consists of three main workflows:

1. Generate a stock ticker list using Polygon.io.
2. Download and store company financial statement data in CSV format.
3. Calculate and rank companies based on financial ratios.

---

## Files

### polygonAPIkey.py

Stores the Polygon.io API key used for authentication.

```python
# -*- coding: utf-8 -*-
"""
polygon.io API secrets
"""

polygonAPIkey = ''
```

---

### fs_ticker_list.py

Retrieves active common stock tickers from Polygon.io and creates a ticker list.

#### Functionality

- Connects to Polygon.io using the API key
- Retrieves active stock tickers
- Sorts ticker symbols alphabetically
- Exports ticker symbols to `symbol_list.csv`

#### Output

```text
symbol_list.csv
```

---

### fs_bulk_downloader.py

Downloads company financial statement data for each ticker in the symbol list.

#### Functionality

- Reads ticker symbols from `symbol_list.csv`
- Requests financial statement data from Polygon.io
- Extracts company information and filing details
- Flattens nested financial statement data structures
- Saves financial statement data as CSV files

#### Output

```text
AAPL.csv
MSFT.csv
GOOGL.csv
...
```

Each CSV file contains:

- Symbol
- CIK
- Company Name
- Filing Date
- Fiscal Period
- Fiscal Year
- Start Date
- End Date
- Source Filing URLs
- Financial Statement Line Items

---

### fs_scanner.py

Calculates and ranks companies using financial statement data.

#### Functionality

- Reads downloaded financial statement CSV files
- Calculates Debt-to-Equity Ratio

```text
Debt-to-Equity Ratio =
Total Liabilities / Total Equity
```

- Filters data for:
  - Fiscal Period: Q3
  - Fiscal Year: 2024
- Removes missing values
- Sorts companies by Debt-to-Equity Ratio

#### Output

```text
symbol | debt_to_equity_ratio
```

Sorted from lowest to highest Debt-to-Equity Ratio.

---

## Requirements

Install required packages:

```bash
pip install polygon-api-client
pip install pandas
pip install plotly
```

---

## Usage

### Step 1: Configure API Key

Add your Polygon.io API key in:

```python
polygonAPIkey = 'YOUR_API_KEY'
```

---

### Step 2: Generate Ticker List

```bash
python fs_ticker_list.py
```

Creates:

```text
symbol_list.csv
```

---

### Step 3: Download Financial Statement Data

```bash
python fs_bulk_downloader.py
```

Downloads financial statement data and saves company CSV files.

---

### Step 4: Run Financial Ratio Scanner

```bash
python fs_scanner.py
```

Calculates Debt-to-Equity Ratios and ranks companies.

---

## Technologies Used

- Python
- Pandas
- Polygon.io API
- polygon-api-client

---

## Author

Rasheeda SUltana
````
