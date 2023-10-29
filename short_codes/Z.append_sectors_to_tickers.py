################################
# The data frequency may not be desirable given the investment schedules.
################################

import os
import pandas as pd

x_bday = 5
path = './traded_tickers_200001_202310'
files = os.listdir(path)

all_tickers = pd.DataFrame()

for x in files:
    spy = pd.read_csv(fr'{path}/{x}')
    spy['Date2'] = pd.to_datetime(spy['Date'])
    spy.set_index('Date2', inplace=True)

    Begin_of_Month = pd.bdate_range('2000-01-01', '2023-10-13', freq='BMS') + pd.offsets.BusinessDay(x_bday)
    try:
        spy = spy.loc[Begin_of_Month]
    except Exception as e:
        print(fr"{x}", e)
        spy = spy.loc[spy.index.isin(Begin_of_Month)]
    spy['Ticker'] = x[:-4]
    all_tickers = pd.concat([all_tickers, spy], ignore_index=True)

all_tickers.to_csv(fr'tickers_{x_bday}days.csv', index=False)