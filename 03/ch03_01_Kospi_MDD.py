import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from scipy import stats
yf.pdr_override()
import matplotlib.pyplot as plt

# 지수 회귀 분석

dow = pdr.get_data_yahoo('^IXIC', '2010-02-11')
kospi = pdr.get_data_yahoo('^KS11', '2010-02-11')

# d = (dow.Close / dow.Close.loc['2000-01-04']) * 100
# k = (kospi.Close / kospi.Close.loc['2000-01-04']) * 100

df = pd.DataFrame({'X': dow['Close'], 'Y' : kospi['Close']})

df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:.2f} * X + {regr.intercept:.2f}'

plt.figure(figsize=(7,7))
plt.plot(df.X, df.Y, '.')
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
plt.legend(['IXIC x KOSPI', regr_line])
plt.title(f'IXIC x KOSPI (R = {regr.rvalue:.2f})')
plt.xlabel('IXIC')
plt.ylabel('KOSPI')
plt.show()

# regr = stats.linregress(df['DOW'], df['KOSPI'])

# df.corr()
#
# r_value = df['DOW'].corr(df['KOSPI'])
#
# r_squared = r_value ** 2
#
# print(r_squared)





# window = 252
# peak= kospi['Adj Close'].rolling(window, min_periods=1).max()
# drawdown = kospi['Adj Close']/peak - 1.0
# max_dd = drawdown.rolling(window, min_periods=1).min()
#
# plt.figure(figsize=(9, 5))
# plt.plot(d.index, d,'r--',  label='Dow Jones Industrial Average')
# plt.plot(k.index, k, 'b', label='KOSPI')
# plt.grid(True)
# plt.legend(loc='best')
# plt.show()

# plt.figure(figsize=(9,7))
# plt.subplot(211)
# kospi['Close'].plot(label='KOSPI', title='KOSPI MDD', grid=True, legend=True)
# plt.subplot(212)
# drawdown.plot(c='blue', label='KOSPI DD', grid=True, legend=True)
# max_dd.plot(c='red', label='KOSPI MDD', grid=True, legend=True)
# plt.show()
