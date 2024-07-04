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

        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if(result[0] is None):
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()
        if (result[0] is None):
            print("start_date : {} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')
