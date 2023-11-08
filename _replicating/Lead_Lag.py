# https://github.com/OpenSourceAP/CrossSection/blob/master/Signals/Code/Predictors/IndRetBig.do

# df = pd.read_excel(fr"./ff49.xlsx") # rows = (df['Date'] >= 200001)
# HML = 1.050, Tstat = 2.584
# decile       1       2       3       4       5       6       7       8       9
# count   283.00  283.00  283.00  283.00  283.00  283.00  283.00  283.00  283.00
# mean      0.25    0.79    0.83    0.83    1.08    1.36    1.40    1.41    1.30
# std       8.11    6.99    7.00    6.23    6.43    6.67    6.44    6.15    6.84
# min     -32.67  -28.77  -29.17  -28.32  -23.38  -21.85  -20.71  -21.87  -19.39
# 25%      -3.80   -2.38   -2.44   -2.74   -2.39   -2.78   -2.43   -1.95   -2.79
# 50%       0.46    0.91    1.02    1.27    1.54    1.75    1.55    1.46    1.44
# 75%       4.70    4.55    4.26    4.25    4.89    5.22    4.75    4.36    4.94
# max      39.02   30.94   33.79   22.54   22.03   31.12   26.52   26.98   38.74
# Tstat     0.52    1.91    1.99    2.24    2.83    3.42    3.64    3.85    3.20

# df = pd.read_excel(fr"./ff49_VW.xlsx") # rows = (df['Date'] >= 200001)
# HML = 0.365, Tstat = 1.060
# decile       1       2       3       4       5       6       7       8       9
# count   283.00  283.00  283.00  283.00  283.00  283.00  283.00  283.00  283.00
# mean      0.62    0.90    0.94    1.02    0.82    0.89    1.06    0.90    0.99
# std       6.72    5.82    5.63    4.86    5.14    4.82    4.88    4.97    5.65
# min     -29.49  -22.90  -23.21  -18.60  -21.75  -19.16  -18.78  -17.38  -16.41
# 25%      -2.79   -1.95   -1.86   -1.50   -1.46   -1.85   -1.52   -1.93   -2.17
# 50%       0.92    1.25    0.98    1.28    1.22    1.36    1.44    1.32    1.08
# 75%       4.21    4.16    4.00    4.10    3.59    3.70    3.94    4.31    4.18
# max      23.64   19.94   22.70   15.33   15.98   12.62   17.97   26.80   24.89
# Tstat     1.56    2.61    2.80    3.52    2.70    3.11    3.67    3.04    2.95

# df = pd.read_excel(fr"./ff49.xlsx") # rows = (df['Date'] >= 196701) & (df['Date'] <= 201612)
# HML = 2.498, Tstat = 8.543
# decile       1       2       3       4       5       6       7       8       9
# count   599.00  599.00  599.00  599.00  599.00  599.00  599.00  599.00  599.00
# mean     -0.51    0.76    0.90    0.91    1.16    1.23    1.55    1.61    1.98
# std       8.29    6.50    6.32    6.09    5.93    6.09    6.07    5.82    6.61
# min     -32.67  -29.15  -24.24  -30.57  -28.13  -29.43  -30.79  -30.70  -29.43
# 25%      -4.14   -2.67   -2.51   -2.49   -2.36   -2.55   -1.96   -2.02   -1.46
# 50%       0.31    0.92    1.02    1.03    1.38    1.35    1.67    1.71    1.78
# 75%       4.15    4.27    4.61    4.54    4.83    4.77    5.06    4.82    5.65
# max      39.02   30.94   35.69   30.49   25.11   31.12   29.38   26.98   38.74
# Tstat    -1.52    2.85    3.50    3.64    4.80    4.96    6.23    6.77    7.34

import os

import pandas as pd
import numpy as np
pd.set_option('display.precision', 2)

os.getcwd()

df = pd.read_excel(fr"./ff49.xlsx")
#rows = (df['Date'] >= 200001)
rows = (df['Date'] >= 196701) & (df['Date'] <= 201612)
cols = [x for x in df.columns if x not in ['Banks', 'Insur', 'RlEst', 'Fin  ']]
df2 = df[rows][cols]

df3 = (df2.set_index('Date') / 100 + 1).rolling(1).apply(np.prod) - 1
df4 = df3.shift(1)
df5 = df4.dropna().apply(lambda x: pd.qcut(x, q=9, labels=range(1,10)), axis=1)

df2_long = pd.melt(df2, id_vars='Date').rename(columns={'value':'ret'})
df5_long = pd.melt(df5.reset_index(), id_vars='Date').rename(columns={'value':'decile'})

df6 = pd.merge(df5_long, df2_long, how='inner', on=['Date', 'variable']).dropna()
df7 = df6.groupby(['Date', 'decile'], as_index=False, observed=False).agg(
    ret=('ret', 'mean'),
    ret_cnt=('ret', 'count')
)
df8 = df7.pivot(index='Date', columns='decile', values='ret' )

df9 = df8.describe()
df9 = df8.describe()
df9.loc['Tstat'] = df9.loc['mean'] / df9.loc['std'] * np.sqrt(df9.loc['count'])

HML = df8[9] - df8[1]

print(fr"HML = {HML.mean():.3f}, Tstat = {HML.mean()/HML.std()*np.sqrt(len(HML)):.3f}")
print(df9)



