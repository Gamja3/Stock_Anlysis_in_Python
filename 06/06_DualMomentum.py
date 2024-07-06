import calendar
import json
from threading import Timer
import pymysql
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from Investar import Analyzer


class DualMomentum:
    def __init__(self):
        """생성자: KRX 종목코드(codes)를 구하기 위한 Market DB 객체 생성"""
        self.mk = Analyzer.MarketDB()

    def get_rltv_momentum(self, start_date, end_date, stock_count):
        """특정 기간 동안 수익률이 제일 높았던 stock_count 개의 종목들 (상대모멘텀)
         - start_date  : 상대 모멘텀을 구할 시작일자 ('2020-01-01')
         - end_date    : 상대 모멘텀을 구할 종료일자 ('2020-12-31')
         - stock_count : 상대 모멘텀을 구할 종목수
         """
        connection = pymysql.connect(host='localhost', user='root', port=3307,
                                     password='1234', db='investar', charset='utf8mb4')
        cursor = connection.cursor()

        sql = f"SELECT MAX(date) FROM daily_price WHERE date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print(f"start_date : {start_date} -> returned None")
            return None
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"SELECT MAX(date) FROM daily_price WHERE date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print(f"end_date : {end_date} -> returned None")
            return None
        end_date = result[0].strftime('%Y-%m-%d')

        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(self.mk.codes):
            sql = (f"SELECT close FROM daily_price "
                   f"WHERE code='{code}' AND date='{start_date}'")
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            old_price = int(result[0])
            sql = (f"SELECT close FROM daily_price "
                   f"WHERE code='{code}' AND date='{end_date}'")
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])

        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        df = df.head(stock_count)
        df.index = range(stock_count)

        connection.close()
        print(df)
        print(f"\nRelative momentum ({start_date} ~ {end_date}): "
              f"{df['returns'].mean():.2f}% \n")
        return df

    def get_abs_momentum(self, rltv_momentum, start_date, end_date):
        """특정 기간 동안 상대 모멘텀에 투자했을 때의 평균 수익률 (절대 모멘텀)
            - rltv_momentum : get_rltv_momentum() 함수의 리턴값 (상대 모멘텀)
            - start_date    : 절대 모멘텀을 구할 매수일 ('2020-01-01)
            - end_date      : 절대 모멘텀을 구할 매도일 ('2020-12-31')
            """
        if rltv_momentum is None:
            print("Relative momentum data is None")
            return

        stockList = list(rltv_momentum['code'])
        connection = pymysql.connect(host='localhost', user='root', port=3307,
                                     password='1234', db='investar', charset='utf8mb4')
        cursor = connection.cursor()

        # 사용자가 입력한 매수일을 DB에서 조회되는 일자로 변경
        sql = (f"SELECT MAX(date) FROM daily_price "
               f"WHERE date <= '{start_date}'")
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print(f"{start_date} -> returned None")
            return
        start_date = result[0].strftime('%Y-%m-%d')

        # 사용자가 입력한 매도일을 DB에서 조회되는 일자로 변경
        sql = (f"SELECT MAX(date) FROM daily_price "
               f"WHERE date <= '{end_date}'")
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] is None:
            print(f"{end_date} -> returned None")
            return
        end_date = result[0].strftime('%Y-%m-%d')

        # 상대 모멘텀의 종목별 수익률을 구해서 2차원 리스트 형태로 추가
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(stockList):
            sql = (f"SELECT close FROM daily_price "
                   f"WHERE code='{code}' AND date='{start_date}'")
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            old_price = int(result[0])
            sql = (f"SELECT close FROM daily_price "
                   f"WHERE code='{code}' AND date='{end_date}'")
            cursor.execute(sql)
            result = cursor.fetchone()
            if result is None:
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])

        # 절대 모멘텀 데이터프레임을 생성한 후 수익률순으로 출력
        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        connection.close()
        print(df)
        print(f"\nAbsolute momentum ({start_date} ~ {end_date}): "
              f"{df['returns'].mean():.2f}% \n")
        return df


dm = DualMomentum()
rm = dm.get_rltv_momentum('2024-01-01', '2024-04-01', 10)  # 수정된 기간

if rm is not None:
    am = dm.get_abs_momentum(rm, '2024-04-01', '2024-12-31')  # 수정된 기간

