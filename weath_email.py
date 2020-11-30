# -*- coding: utf-8 -*-
# @Time    : 2020/11/27 17:16
# @Author  : Walton
# @FileName: weath_email.py
# @Software: PyCharm
# @Blog    ：https://www.waltonzhong.com

#!/usr/bin/python3.6
# coding=UTF-8

import datetime
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

url = 'https://free-api.heweather.net/s6/weather/forecast?location=深圳&key=684670d3c7604b41afebcf3111c216ec'
# 获取当日时间  2019-11-10
# today_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
sender = 'vontenccie@163.com'
passw = 'HAGUTMMTGFSJDSSA'
mail_host = 'smtp.163.com'
receivers = ['717708723@qq.com','664769979@qq.com']

def get_weather_data():
    res = requests.get(url).json()
    # res.encoding = 'utf-8'
    result = res['HeWeather6'][0]['daily_forecast']
    location = res['HeWeather6'][0]['basic']
    city =location['location']
    data = result[1]
    info = {
        'city': city,
        'date': data['date'],
        'tmp_max': data['tmp_max'],
        'tmp_min': data['tmp_min'],
        'cond_txt_d': data['cond_txt_d'],
        'cond_txt_n': data['cond_txt_n'],
        'hum': data['hum'],
        'sr': data['sr'],
        'ss': data['ss'],
        'mr': data['mr'],
        'ms': data['ms'],
        'pop': data['pop'],
        'pcpn': data['pcpn'],
        'uv_index': data['uv_index'],
        'vis': data['vis'],
        'wind_dir': data['wind_dir'],
        'wind_sc': data['wind_sc'],
        'wind_spd': data['wind_spd'],
    }
    # send_email()
    # auto_email()
    return info

def auto_email():
    msg = MIMEMultipart()
    msg['Subject'] = '%s 天气预报信息来啦！' % tomorrow
    msg['From'] = sender
    data = get_weather_data()
    message = """
    <html><body><h1>{date} 天气预报</h1>
    <p><strong>城市：</strong>{city}</p>
    <p><strong>最高气温：</strong>{tmp_max}</p>
    <p><strong>最低气温：</strong>{tmp_min}</p>
    <p><strong>白天天气状况：</strong>{cond_txt_d}</p>
    <p><strong>夜间天气状况：</strong>{cond_txt_n}</p>
    <p><strong>相对湿度：</strong>{hum}</p>
    <p><strong>日出时间：</strong>{sr}</p>
    <p><strong>日落时间：</strong>{ss}</p>
    <p><strong>降水概率：</strong>{pop}</p>
    <p><strong>降水量：</strong>{pcpn}</p>
    <p><strong>紫外线强度：</strong>{uv_index}</p>
    <p><strong>能见度/公里：</strong>{vis}</p>
    <p><strong>风向：</strong>{wind_dir}</p>
    <p><strong>风力：</strong>{wind_sc}</p>
    <p><strong>风速(公里/小时)：</strong>{wind_spd}</p>
    """.format(date=data['date'], city=data['city'],  tmp_max=data['tmp_max'],
               tmp_min=data['tmp_min'], cond_txt_d=data['cond_txt_d'],  cond_txt_n=data['cond_txt_n'],
               hum=data['hum'], sr=data['sr'],  ss=data['ss'],
               pop=data['pop'],
               pcpn=data['pcpn'], uv_index=data['uv_index'],  vis=data['vis'],
               wind_dir=data['wind_dir'], wind_sc=data['wind_sc'],  wind_spd=data['wind_spd'],)
    message_html = MIMEText(message, 'html', 'utf-8')
    msg.attach(message_html)
    try:
        s = smtplib.SMTP_SSL(mail_host, '465')
        #s.connect(mail_host)
        s.login(sender,passw)
        # s.set_debuglevel(1)
        msg['To'] = ','.join(receivers)
        # msg['Cc'] = ','.join(cc_list)
        receive = receivers
        # receive.extend(cc_list)
        s.sendmail(sender,receive,msg.as_string())
        # print('Success!')
        s.quit()
        print('邮件发送完成！')
    except smtplib.SMTPException as e:
        print('发送失败，原因如下：%s' % e)

if __name__ == '__main__':
    info = auto_email()