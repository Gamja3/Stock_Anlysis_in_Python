import ctypes
import os

import pandas as pd
import win32com.client
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime

#CREON Plus 공통 Object
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')  #시스템 상태 정보
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')  #주문 관련 도구


#CREON Plus 시스템 점검 함수
def check_creon_system():
    #관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print('check_creon_sysytem() : admin user -> FAILED')
        return False

    # 연결 여부 체크
    if cpStatus.IsConnect == 0:
        print('check_creon_sysytem() : connect to server -> FAILED')
        return False

    #주문 관련 초기화
    if cpTradeUtil.TradeInit(0) != 0:
        print('check_creon_sysytem() : init trade -> FAILED')
        return False

    return True


#슬랙
slack_token = 'xoxb-7370805081367-7387853963652-cDeIJmoENIp3yNg0Flcu1EW4'
client = WebClient(token=slack_token)


def dbgout(message):
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbut = datetime.now().strftime('[%m/%d %H:%M:%S]') + message
    try:
        response = client.chat_postMessage(
            channel='C07BDREUSKE',  # 채널 id를 입력합니다.
            text=strbut)
    except SlackApiError as e:
        assert e.response["error"]


def printlog(message, *args):
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


cpStock = win32com.client.Dispatch('DsCbo1.StockMst')  #주식 종목별 정보


def get_current_price(code):
    cpStock.SetInputValue(0, code)  #종목코드에 대한 가격 정보
    cpStock.BlockRequest()

    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11)  #현재가
    item['ask'] = cpStock.GetHeaderValue(16)  #매수호가
    item['bid'] = cpStock.GetHeaderValue(17)  #매도호가

    return item['cur_price'], item['ask'], item['bid']


# OHLC 조회
cpOhlc = win32com.client.Dispatch('CpSysDib.StockChart')


def get_ohkc(code, qty):
    cpOhlc.SetInputValue(0, code)  #종목코드
    cpOhlc.SetInputValue(1, ord('2'))  # 1:기간, 2:개수
    cpOhlc.SetInputValue(4, qty)  #요청 개수
    cpOhlc.SetInputValue(5, [0, 2, 3, 4, 5])  # 0:날짜, 2~5:OHLC
    cpOhlc.SetInputValue(6, ord('D'))  # D: 일단위
    cpOhlc.SetInputValue(9, ord('1'))  # 0:무수정주가, 1:수정주가
    cpOhlc.BlockRequest()

    count = cpOhlc.GetHeaderValue(3)  # 3:수신 개수
    columns = ['open', 'high', 'low', 'close']
    index = []
    rows = []
    for i in range(count):
        index.append(cpOhlc.GetDataValue(0, i))
        rows.append([cpOhlc.GetDataValue(1, i), cpOhlc.GetDataValue(2, i),
                     cpOhlc.GetdataValue(3, i), cpOhlc.GetDataValue(4, i)])

    df = pd.DataFrame(rows, columns=columns, index=index)
    return df


#주식 잔고 조회
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')  # 주문 관련 도구
cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033')  # 계좌 정보
cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode')  # 종목코드

# def get_stock_balance(code):


if __name__ == '__main__':
    # crs = check_creon_system()
    # print(crs)
    # dbgout('This is test log.')
    creon_id = os.environ.get('CREON_ID')
    print(creon_id)

    # print(get_ohkc('A305080', 10))

# obj = win32com.client.Dispatch("DsCbo1.StockMst")
# obj.SetInputValue(0, 'A005930')
# obj.BlockRequest()
# sec = {}
# sec['현재가'] = obj.GetHeaderValue(11)
# sec['전일대비'] = obj.GetHeaderValue(12)
# print(sec)
