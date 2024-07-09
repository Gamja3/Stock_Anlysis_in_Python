import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import requests
import mplfinance as mpf

krx_list = pd.read_html('C:\myPackage\chapter3\상장법인목록.xls')

krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format)

# print(krx_list[0])

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')
# print(pgrr.a['href'])
# print(pgrr.prettify())

s = pgrr.a['href'].split('=')
last_page = s[-1]
print(last_page)


df_list = []
df = pd.DataFrame()
site_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    url = '{}&page={}'.format(site_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = pd.read_html(html, header=0)[0]
    # df = df.append(pd.read_html(html, header=0)[0])
    df_list.append(df)

# 데이터프레임 결합
df = pd.concat(df_list, ignore_index=True)
df = df.dropna()

df = df.iloc[0:30]
# df = df.sort_values(by='날짜')
df = df.rename(columns={'날짜': 'Date', '시가': 'Open', '고가': 'High', '저가': 'Low', '종가': 'Close', '거래량': 'Volume'})
df = df.sort_values(by='Date')

# 날짜를 인덱스로 설정하고 필요한 열 선택
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]

kwargs = dict(title='Celltrion candle chart', type='candle',
              mav=(2, 4, 6), volume=True, ylabel='ohlc candles')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)


# mpf.plot(df, title='Celltrion candle chart', type='ohlc')

# plt.title('celltrion')
# plt.xticks(rotation=45)
# plt.plot(df['날짜'], df['종가'], 'co-')
# plt.grid(color='gray', linestyle='--')
# plt.show()
