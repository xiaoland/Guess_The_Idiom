#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:xiaoland
# create_time: 2018/6/1

import os
import sys
import json
import requests
import urllib
import urllib2
import httplib
from dueros.duerskills.BotServer import application
from dueros.Bot import Bot
from dueros.card.ImageCard import ImageCard 
from dueros.card.ListCard import ListCard
from dueros.card.ListCardItem import ListCardItem
from dueros.card.StandardCard import StandardCard
from dueros.card.TextCard import TextCard

class guess(Bot):
    
    def __init__(self, data):
        
        super().__init__(data)
        self.number = random.randint(0,67)
        self.addLaunchHandler(self.launchRequest)
        self.addIntentHandler('express_id', self.express_id)
        self.addIntentHandler('ai.dueros.common.default_intent', self.quesheng)
        
    def launchRequest(self):
        
        return {
            'card': TextCard('说出“开始猜成语”即可开始看图猜成语'),
            'outputSpeech': r'来啊，猜成语啊，说出，开始猜成语，即可开始看图猜成语'
        }
        
    
    def quesheng(self):
        
        card = ImageCard()
        card.addItem(self.imageurl[self.number][1])
        card.addCueWords('小度小度，我觉得答案是......')
        card.addCueWords('小度小度，我认为答案是......')
        return {
            'card': card,
            'outputSpeech': r'你说的好像不是快递单号哦，请说出您的快递单号'
        }
    
    def express_id(self):
        
        id = self.getSlots('sys.number')
        if id == None or id == '':
            self.nlu.ask('sys.number')
        requestData = {
                   'OrderCode': id,
                   'ShipperCode':'YTO',
                   'LogisticCode':'12345678'
        }
    
        data = {
                'EBusinessID': '1349773',
                'RequestType': '1002',
                'RequestData': urllib.urlencode(str(requestData)) ,
                'DataType': '2',
        }
        hash.update(str(requestData) + '1f0c5c35-67a8-495f-b3ab-a7fc534a826f', encoding='utf-8')
        data['DataSign'] = urllib.urlencode(base64.b64encode(hash.hexdigest()))
        r = requests.post('http://api.kdniao.cc/Ebusiness/EbusinessOrderHandle.aspx',
                          data=data,
                          headers='application/x-www-form-urlencoded;charset=utf-8')
        json = r.json()
        try:
            card = TextCard(json['Traces'][-1]['AcceptStation'])
            return {
                'card': card,
                'outputSpeech': json['Traces'][-1]['AcceptStation']
            }
        except KeyError:
            card = TextCard('对不起，包裹信息查询失败')
            return {
                'card': card,
                'outputSpeech': '对不起，包裹信息查询失败'
            }
    

    
if __name__ == '__main__':
    
    pass
    
