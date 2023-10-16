
################################
# The data frequency may not be desirable given the investment schedules.
# this code is used for daily data and to select the x-th business day of each month
################################
import pandas as pd

x_bday = 5
spy = pd.read_csv('SPY.csv')
spy['Date2'] = pd.to_datetime(spy['Date'])
spy.set_index('Date2', inplace=True)

Begin_of_Month = pd.bdate_range('1993-01-29', '2023-10-13', freq='BMS') + pd.offsets.BusinessDay(x_bday)
try:
    spy = spy.loc[Begin_of_Month]
except Exception as e:
    print(e)
    spy = spy.loc[spy.index.isin(Begin_of_Month)]

spy.to_csv(fr"SPY_{x_bday}bday.csv", index=False)
