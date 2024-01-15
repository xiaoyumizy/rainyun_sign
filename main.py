import requests
import json
import telepot
import os

#Api信息
tgpush = 'true'

# 获取私密仓库变量
api_key = os.environ.get('API_KEY')
bot_token = os.environ.get('BOT_TOKEN')
chat_id = os.environ.get('CCHAT_ID')

#请求用户信息
url = "https://api.v2.rainyun.com/user/"
payload={}
headers_yh = {
   'X-Api-Key': api_key
}
res_points = requests.request("GET", url, headers=headers_yh, data=payload)
zh_json = res_points.json()
pointsbefore = zh_json['data']['Points']
ID = zh_json['data']['ID']
name = zh_json['data']['Name']
print(f'ID：{ID}')
print(f'用户名：{name}')
print(f'剩余积分：{pointsbefore}')
print('==============================')
#签到部分
url_lqjf = 'https://api.v2.rainyun.com/user/reward/tasks'
headers_lqjf = {
    'content-type':"application/json",
    'X-Api-Key':api_key
    }
body_lqjf = {
    "task_name" : '每日签到',
    "verifyCode" : ''
    }
res_lqjf = requests.request("POST", url_lqjf, headers=headers_lqjf, data = json.dumps(body_lqjf))
res_points = requests.request("GET", url, headers=headers_yh, data=payload)
zh_json = res_points.json()
points = zh_json['data']['Points']
if points == {pointsbefore + 300}:
    print(f'签到成功，当前剩余积分：{points + 300}')
else:
    print(f'签到失败，返回值：{res_lqjf.text}')
print('==============================')
try:
   #推送
   requests.request("GET"，f'https://api.telegram.org/bot{bot_token}/sendmessage?chat_id={chat_id}&text=傻逼雨云自动签到\n用户ID：{ID}\n用户名：{name}\n签到前积分：{pointsbefore}\n当前积分：{points}\n签到结果\n<pre>{res_lqjf.text}</pre>&parse_mode=HTML')
except Exception as e:
    print(f"发生了一个错误: {e}")
