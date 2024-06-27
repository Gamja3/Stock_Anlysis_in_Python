import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from Investar import Analyzer

# MarketDB 객체 생성
mk = Analyzer.MarketDB()

# 삼성전자 데이터 가져오기
df = mk.get_daily_price('삼성전자', '2000-01-01', '2024-06-26')

# 액면분할 발생일 및 비율
split_date = datetime.strptime('2018-05-04', '%Y-%m-%d').date()
split_ratio = 50

# 액면분할 조정
df.loc[df.index <= split_date, 'close'] /= split_ratio

# 수익률 계산
df['daily_ret'] = df['close'].pct_change()
df['cum_ret'] = (1 + df['daily_ret']).cumprod() - 1

# RSI 계산 함수
def calculate_RSI(data, window=14):
    delta = data['close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    RS = avg_gain / avg_loss
    RSI = 100 - (100 / (1 + RS))

    return RSI

# RSI 계산
df['RSI'] = calculate_RSI(df)

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(12, 6))

# 주가를 표시하는 y축
ax1.plot(df.index, df['close'], color='blue', label='Close Price')
ax1.set_xlabel('Date')
ax1.set_ylabel('Close Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# RSI를 표시하는 y축
ax2 = ax1.twinx()
ax2.plot(df.index, df['RSI'], color='orange', label='RSI')
ax2.axhline(70, color='red', linestyle='--')
ax2.axhline(30, color='green', linestyle='--')
ax2.set_ylabel('RSI', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

fig.tight_layout()
plt.title('삼성전자 종가 및 RSI (액면분할 조정)')
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.show()
