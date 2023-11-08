# https://github.com/OpenSourceAP/CrossSection/blob/master/Signals/Code/Predictors/IndMom.do

# df = pd.read_excel(fr"ff49.xlsx")
# rows = (df['Date'] >= 200001)
# HML = 1.215, Tstat = 3.023
# decile        1        2        3        4  ...        6        7        8        9
# count   278.000  278.000  278.000  278.000  ...  278.000  278.000  278.000  278.000
# mean      0.471    0.642    0.828    0.932  ...    1.013    1.153    1.305    1.687
# std       8.835    7.046    6.950    6.497  ...    6.226    6.186    6.070    6.524
# min     -34.348  -26.682  -26.402  -22.720  ...  -31.102  -23.036  -26.228  -19.680
# 25%      -4.043   -3.220   -3.201   -2.474  ...   -1.701   -2.019   -1.980   -2.478
# 50%       0.293    0.826    0.859    1.067  ...    1.314    1.283    1.474    1.308
# 75%       4.478    4.548    4.136    4.115  ...    4.429    4.427    4.875    5.471
# max      44.200   34.106   35.756   27.304  ...   22.062   31.778   19.178   26.420
# Tstat     0.889    1.519    1.987    2.393  ...    2.713    3.107    3.584    4.311

# df = pd.read_excel(fr"ff49_VW.xlsx"); rows = (df['Date'] >= 200001)
# HML = 0.926, Tstat = 2.336
# decile        1        2        3        4  ...        6        7        8        9
# count   278.000  278.000  278.000  278.000  ...  278.000  278.000  278.000  278.000
# mean      0.436    0.898    0.729    0.915  ...    1.060    0.905    0.876    1.362
# std       7.522    6.148    5.150    4.893  ...    4.721    4.765    4.802    5.642
# min     -32.782  -25.094  -22.846  -18.824  ...  -16.890  -18.498  -19.248  -18.498
# 25%      -3.047   -2.164   -1.615   -1.470  ...   -1.655   -1.746   -1.752   -1.726
# 50%       0.419    1.381    1.162    1.287  ...    1.516    1.119    1.393    1.442
# 75%       4.111    3.824    3.676    4.167  ...    3.992    3.835    3.842    4.855
# max      35.228   31.194   22.336   16.794  ...   13.042   14.240   17.376   21.800
# Tstat     0.966    2.436    2.360    3.119  ...    3.743    3.168    3.043    4.025

# df = pd.read_excel(fr"ff49.xlsx") # rows = (df['Date'] >= 197001) & (df['Date'] <= 201612)
# HML = 1.500, Tstat = 5.716
# decile        1        2        3        4  ...        6        7        8        9
# count   558.000  558.000  558.000  558.000  ...  558.000  558.000  558.000  558.000
# mean      0.557    0.845    1.025    1.056  ...    1.283    1.312    1.638    2.057
# std       7.600    6.502    6.318    6.134  ...    5.723    5.677    6.009    6.592
# min     -34.348  -27.494  -28.356  -30.018  ...  -28.216  -29.238  -28.564  -30.016
# 25%      -3.259   -2.658   -2.554   -2.430  ...   -2.138   -1.764   -1.842   -1.638
# 50%       0.476    0.847    1.107    1.136  ...    1.455    1.395    1.759    1.772
# 75%       4.180    4.563    4.175    4.246  ...    4.771    4.756    5.128    5.323
# max      44.200   34.106   35.756   33.694  ...   20.922   27.818   25.120   40.836
# Tstat     1.731    3.071    3.831    4.067  ...    5.297    5.457    6.439    7.372

import os

import pandas as pd
import numpy as np
from scipy.stats import mstats
pd.set_option('display.precision', 3)

os.getcwd()

df = pd.read_excel(fr"ff49.xlsx")
rows = (df['Date'] >= 200001)
#rows = (df['Date'] >= 197001) & (df['Date'] <= 201612)
cols = [x for x in df.columns if x not in ['Banks', 'Insur', 'RlEst', 'Fin  ']]
df2 = df[rows][cols]
#df2 = df2.apply(lambda x: mstats.winsorize(x, limits=[0.001, 0.001]), axis=0)

df3 = (df2.set_index('Date') / 100 + 1).rolling(6).apply(np.prod) - 1
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
df9.loc['Tstat'] = df9.loc['mean'] / df9.loc['std'] * np.sqrt(df9.loc['count'])

HML = df8[9] - df8[1]

print(fr"HML = {HML.mean():.3f}, Tstat = {HML.mean()/HML.std()*np.sqrt(len(HML)):.3f}")
print(df9)


