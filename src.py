#coding = utf-8

import requests
import bs4
import time
import schedule
import json
from wxpy import *

#天气地址
hangzhou = "http://t.weather.sojson.com/api/weather/city/101210101"#杭州
#发送时间
send_time = ["07:10"]

#登录网页微信并保持在线
bot = Bot(console_qr = 1,cache_path="cache.wx")
#获取html文件
def get_html(url):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
            'ContentType':
            'text/html; charset=utf-8',
            'Accept-Encoding':
            'gzip, deflate, sdch',
            'Accept-Language':
            'zh-CN,zh;q=0.8',
            'Connection':
            'keep-alive',
    }
        try:
            response = requests.get(url, headers = headers, timeout = 100)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except:
            return " 请求失败 "
#获得天气信息
def get_weather(response):
    if(response == " 请求失败 "):
        print("请求失败")
    else:
    # 今日信息
        data = json.loads(response)
        city = data['cityInfo']['city']
        today = data['data']['forecast'][0]['ymd']
        today_hightem = data['data']['forecast'][0]['high']
        today_lowtem = data['data']['forecast'][0]['low']
        today_win = data['data']['forecast'][0]['fx']+' '+data['data']['forecast'][0]['fl']
        today_wea = data['data']['forecast'][0]['type']
        notice = data['data']['forecast'][0]['notice']
        today_data = '['+ today +']' + '\n' + city + '\n' + today_hightem  + '/' + today_lowtem + '\n' + '天气：' + today_wea + '\n' + '风力：' + today_win + '\n'
        info = [today_data, notice]
        return info
 #获取金山词霸每日一句，英文和翻译
def get_news():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    onewords = r.json()['content']
    note = r.json()['note']
    return onewords, note

# 计算天数 
def get_days(): 
    #time1是开始的时间 
    time1 = "2018-08-10" 
    time2 = datetime.datetime.now().strftime('%Y-%m-%d') 
    day1 = time.strptime(str(time1), '%Y-%m-%d') 
    day2 = time.strptime(str(time2), '%Y-%m-%d') 
    days = (int(time.mktime(day2)) - int(time.mktime(day1))) / (24 * 60 * 60) 
    return abs(int(days))

def run():
    response = get_html(hangzhou)
    info = get_weather(response)
    news = get_news()
    sendMgs("fyatto",news[0])
    sendMgs("fyatto",news[1])
    sendMgs("fyatto",info[0] + '\n' + "温馨提示:" +info[1])
    


#指定好友发送指定内容
def sendMgs(user,content):
    my_friend = bot.friends().search(user)[0]
    my_friend.send(content)
#保持运行
schedule.every().day.at(send_time[0]).do(run)
while True:
    schedule.run_pending()
    time.sleep(1)
bot.join()
