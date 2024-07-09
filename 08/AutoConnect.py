import os
import time
import sys
from pywinauto import application
from dotenv import load_dotenv

os.system('chcp 65001')
os.system('dir/w')

# .env 파일 로드
load_dotenv()

# 환경 변수에서 로그인 정보 가져오기
creon_id = os.environ['CREON_ID']
creon_password = os.environ['CREON_PASSWORD']
creon_cert_password = os.environ['CREON_CERT_PASSWORD']

# 기존 프로세스 종료
os.system('taskkill /IM coStarter* /F /T')
os.system('taskkill /IM CpStart* /F /T')
os.system('taskkill /IM DibServer* /F /T')
os.system('wmic process where "name like \'%coStarter%\'" call terminate')
os.system('wmic process where "name like \'%CpStart%\'" call terminate')
os.system('wmic process where "name like \'%DibServer%\'" call terminate')

time.sleep(5)

# 애플리케이션 시작
app = application.Application()
app.start(f'C:\\CREON\\STARTER\\coStarter.exe /prj:cp /id:{creon_id} /pwd:{creon_password} /pwdcert:{creon_cert_password} /autostart/')
time.sleep(60)
