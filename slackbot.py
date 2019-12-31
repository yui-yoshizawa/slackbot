# -*- coding: utf-8 -*-
from slacker import Slacker
import requests
from configparser import ConfigParser

class Config(object):
    def __init__(self, conf):
        self.conf = conf
        self.SLACK_TOKEN = conf["DEFAULT"]["SLACK_TOKEN"]

class Weather(object):
    def get_weather(self, city_id):
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'
        tmp_url = url.format(city_id)

        tmp_response = requests.get(tmp_url)
        res = tmp_response.json()
        forecasts = res['forecasts']

        return forecasts

class GetParameter(object):
    def get_parameter(self, weather_result, date):
        if date == 'today':
            num = 0
        elif date == 'tomorrow':
            num = 1
        
        weather = weather_result[num]
        parameter = {}
        parameter['date_label'] = weather['dateLabel']
        parameter['telop'] = weather['telop']
        parameter['date'] = weather['date']


        if weather['temperature']['min'] == None:
            parameter['temperature_min'] = '--'
        else:
            parameter['temperature_min'] = weather['temperature']['min']['celsius']
        
        if weather['temperature']['max'] == None:
            parameter['temperature_max'] = '--'
        else:
            parameter['temperature_max'] = weather['temperature']['max']['celsius']

        return parameter

class Message(object):
    def make_message(self, data, city):

        telop_icon = ''
        if data['telop'].find('雪') > -1:    
            telop_icon = ':showman:'
        elif data['telop'].find('雷') > -1:
            telop_icon = ':thinder_cloud_and_rain:'
        elif data['telop'].find('晴') > -1:
            if data['telop'].find('曇') > -1:
                telop_icon = ':partly_sunny:'
            elif data['telop'].find('雨') > -1:
                telop_icon = ':partly_sunny_rain:'
            else:
                telop_icon = ':sunny:'
        elif data['telop'].find('雨') > -1:
            telop_icon = ':umbrella:'
        elif data['telop'].find('曇') > -1:
            telop_icon = ':cloud:'
        else:
            telop_icon = ':fire:'

        temperature_icon = ':thermometer:'
        message = 'おはよう！\n' + data['date_label'] + 'の' + city + 'の天気をお知らせするよ！\n' + '\n' + telop_icon + data['date_label'] + 'の天気は【' + data['telop'] + '】だよ！\n' + temperature_icon + '最低気温: ' +  data['temperature_min'] + '℃  最高気温: ' + data['temperature_max'] + '℃'

        return message

class Slack(object):
    def send_message(self, message, slack):
        slack.chat.post_message('zz_slackbot_test', message, as_user=True)

if __name__ == "__main__":
    config = ConfigParser()
    config.read('/Users/yoshizawa/practice/practice_slackbot/conf/bot.conf')
    c = Config(config)

    w = Weather()    # インスタンス化
    city = '東京'
    city_id = 130010    # 東京のID
    weather_result = w.get_weather(city_id)

    gp = GetParameter()    # インスタンス化
    date = 'today'    # 今日のデータをとってくる
    data = gp.get_parameter(weather_result, date)

    m = Message()
    message = m.make_message(data, city)

    slack_token = c.SLACK_TOKEN
    print(slack_token)
    slack = Slacker(slack_token)

    s = Slack()
    s.send_message(message, slack)