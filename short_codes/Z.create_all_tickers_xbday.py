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
    windows = spy['Adj Close'].rolling(260)
    spy['Week52_high'] = windows.max()
    spy['Week52_low'] = windows.min()
    for size in [21, 63, 126]:
        windows = spy['Volume'].rolling(size)
        spy['vol_MA'+str(size)] = windows.mean()
        spy['vol_zero'+str(size)] = windows.apply(lambda x: (x==0).sum())

    Begin_of_Month = pd.bdate_range('2000-01-01', '2023-10-13', freq='BMS') + pd.offsets.BusinessDay(x_bday)
    try:
        spy = spy.loc[Begin_of_Month]
    except Exception as e:
        print(fr"{x}", e)
        spy = spy.loc[spy.index.isin(Begin_of_Month)]
    spy['Ticker'] = x[:-4]
    # added on 10/28/2023

    spy['avg_price'] = spy[['Open', 'High', 'Low', 'Close']].mean(axis=1)
    vars = ['Ticker', 'Date', 'avg_price',
            'Adj Close', 'Week52_high', 'Week52_low',
            'Volume', 'vol_MA21', 'vol_MA63', 'vol_MA126', 'vol_zero21', 'vol_zero63', 'vol_zero126']
    all_tickers = pd.concat([all_tickers, spy[vars]], ignore_index=True)

all_tickers.to_csv(fr'tickers_{x_bday}days.csv', index=False)
all_tickers.to_parquet(fr"tickers_{x_bday}days.parquet", compression='zstd', index=False)
