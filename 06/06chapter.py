import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Investar import Analyzer
from datetime import datetime

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', 'NAVER', '현대자동차']
# stocks = ['삼성전자']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2018-10-26', '2024-04-26')['close']

daily_ret = df.pct_change()
annual_ret = daily_ret.mean() * 252
daily_cov = daily_ret.cov()
annual_cov = daily_cov * 252

# 액면분할 발생일 및 비율
split_date = datetime.strptime('2018-05-04', '%Y-%m-%d').date()
split_ratio = 50

# 액면분할 조정
df.loc[df.index <= split_date, '삼성전자'] /= split_ratio

port_ret = []
port_risk = []
port_weights = []
sharpe_ratio = []

for _ in range(20000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    returns = np.dot(weights, annual_ret)
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)
    port_risk.append(risk)
    port_weights.append(weights)
    sharpe_ratio.append(returns / risk)

portfolio = {'Returns': port_ret, 'Risk': port_risk, 'Sharpe': sharpe_ratio}

for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk', 'Sharpe'] + [s for s in stocks]]

max_sharpe = df.loc[df['Sharpe'] == df['Sharpe'].max()]
min_risk = df.loc[df['Risk'] == df['Risk'].min()]

print("max_sharpe\n\n", max_sharpe)
print('min_risk\n\n', min_risk)

df.plot.scatter(x='Risk', y='Returns', c='Sharpe', cmap='viridis',
                edgecolor='k', figsize=(11, 7), grid=True)
plt.scatter(x=max_sharpe['Risk'], y=max_sharpe['Returns'], c='r',
            marker='*', s=300)
plt.scatter(x=min_risk['Risk'], y=min_risk['Returns'], c='r',
            marker='X', s=200)
plt.title('Portfolio Optimization')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show()
