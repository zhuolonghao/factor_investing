
################################
# this code is used to add sector information to tickers
################################

import pandas as pd

target_file = "tickers_5days"
all_tickers = pd.read_csv(fr"{target_file}.csv").drop_duplicates()
sector = pd.read_csv('ProductDetailsHoldings_Total_Stock_Market_ETF.csv').drop_duplicates()

vars_of_interest = ['Ticker', 'Sector', 'Market']
sector = sector[vars_of_interest]

all_tickers = all_tickers.merge(sector, how='inner', left_on='Ticker', right_on='Ticker')
all_tickers.to_csv(fr'{target_file}_sector.csv', index=False)
