from numpy import cumprod
from pandas_datareader import data as pdr
import yfinance as yf
import matplotlib.pyplot as plt
yf.pdr_override()

sec = pdr.get_data_yahoo('005930.KS', start='2018-05-04')
sec_dpc = (sec['Close'] / sec['Close'].shift(1) - 1) * 100
sec_dpc.iloc[0] = 0
sec_dpc_cp = ((100+sec_dpc)/100).cumprod()*100-100

msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')
msft_dpc = (msft['Close'] / msft['Close'].shift(1) - 1) * 100
msft_dpc.iloc[0] = 0
msft_dpc_cp = ((100+msft_dpc)/100).cumprod()*100-100

plt.plot(sec.index, sec_dpc_cp, 'b', label='Samsung Electorinics')
plt.plot(msft.index, msft_dpc_cp, 'r--', label='Microsoft')
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()
# plt.hist(sec_dpc, bins=18)
# plt.grid(True)
# plt.show()
print(sec_dpc_cp)




# plt.plot(sec.index, sec.Close, 'b', label='Samsung Electronics')
# plt.plot(msft.index, msft.Close, 'r--', label='Microsoft')
# plt.legend(loc='best')
# plt.show()

