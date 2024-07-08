from datetime import datetime
import backtrader as bt
import yfinance as yf


class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # 21일 단순 이동평균에 대한 RSI_SMA
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY  : 주가 {order.executed.price:,.0f}  '
                         f'수량 {order.executed.size:,.0f}  '
                         f'수수료 {order.executed.comm:,.0f}  '
                         f'자산 {cerebro.broker.getvalue():,.0f} KRW  '
                         f'RSI {self.rsi[0]:.2f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'SELL : 주가 {order.executed.price:,.0f}  '
                         f'수량 {order.executed.size:,.0f}  '
                         f'수수료 {order.executed.comm:,.0f}  '
                         f'자산 {cerebro.broker.getvalue():,.0f} KRW  '
                         f'RSI {self.rsi[0]:.2f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELED')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')


cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# yfinance를 사용하여 데이터를 가져와서 backtrader에 추가
data = bt.feeds.PandasData(dataname=yf.download('034220.KS',
                                                start='2017-01-01',
                                                end='2024-12-01',
                                                auto_adjust=True))

cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0014)  # ④ 수수료 차감
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)  # ⑤ 매매 주문 적용 주식수

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot(style='candlestick')
