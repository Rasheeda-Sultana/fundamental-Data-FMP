#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# fundamental data scanner

# Import modules
import os 
import pandas as pd

download_path = '/Users/Username/Desktop/fundamental_scan/fundamental_data/'

file_names = [f for f in os.listdir(download_path) if f.endswith('.csv')]

ratio_data = {}

for file in file_names:
    fs_data = pd.read_csv(f'{download_path}{file}')
    fs_data['debt_to_equity_ratio'] = fs_data.financials_balance_sheet_liabilities_value / fs_data.financials_balance_sheet_equity_value 
    
    # Filter the dataframe for the specific conditions
    data_point = fs_data.loc[
        (fs_data['fiscal_period'] == 'Q3') & (fs_data['fiscal_year'] == 2024), 
        'debt_to_equity_ratio'
    ]

    debt_to_equity_ratio = data_point.iloc[0] if not data_point.empty else None
    
    ratio_data[file[:-4]] = debt_to_equity_ratio
    
ratio_dataframe = pd.DataFrame(list(ratio_data.items()), columns=['symbol', 'debt_to_equity_ratio'])
ratio_dataframe = ratio_dataframe.dropna()
ratio_dataframe = ratio_dataframe.sort_values('debt_to_equity_ratio', axis=0, ignore_index=True)
