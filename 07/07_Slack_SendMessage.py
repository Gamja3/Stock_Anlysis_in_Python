from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

os.system('chcp 65001')
# .env 파일 로드
load_dotenv()

slack_api = os.environ['SLACK_API']

slack_token = slack_api
client = WebClient(token=slack_token)

markdown_text= '''
This message is plain.
*This message is bold.*
 'This message is code.'
 _This message is italic._
 ~This message is strike.~
 '''
attach_dict = dict(color='#ff0000', author_name='INVESTAR',
                   author_link='github.com/invester',
                   title='오늘의 증시 KOSPI',
                    title_link='http://finance.naver.com/site/sise_index.nhn?code=KOSPI',
                    text='2,326.13 11.89 (0.51%)',
                    image_url='https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png')

attach_list = [attach_dict]

# response = client.auth_test()
# print(response)


try:
    response = client.chat_postMessage(
        channel="C07BDREUSKE",  # 채널 id를 입력합니다.
        text= markdown_text,attachments=attach_list
    )
except SlackApiError as e:
    assert e.response["error"]