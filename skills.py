#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:xiaoland
# create_time: 2018/6/1

import os
import sys
import json
import requests
import random
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
        self.addIntentHandler('welcome', self.welcome)
        self.addIntentHandler('idiom', self.idiom)
        self.addIntentHandler('c_idiom', self.cidiom)
        self.addIntentHandler('howlg', self.howlg)
        self.addIntentHandler('idiom_answer', self.answeridiom)
        self.addIntentHandler('answerunknow', self.answerunknow)
        self.addIntentHandler('answerhelp', self.answerunknow)
        self.addIntentHandler('ai.dueros.common.default_intent', self.quesheng)
        self.imageurl = [
            ['支离破碎', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%94%AF%E7%A6%BB%E7%A0%B4%E7%A2%8E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A12Z%2F-1%2F%2Ffe3796074d45a645faac8f230a2b5890e8a7dfcd370862dc3acb416e2c05ab26'],
            ['重蹈复辙', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%87%8D%E8%B9%88%E5%A4%8D%E8%BE%99.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A11Z%2F-1%2F%2F30b90339f52f9b742a19f8b013cb034bfe6cd03077daae2b0efbe08049811850'],
            ['一石二鸟', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%80%E7%9F%B3%E4%BA%8C%E9%B8%9F.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A10Z%2F-1%2F%2F8076a49bd6bcc01f444ffac83389ed6617953a39fd15dff853331198fc6da12b'],
            ['一叶障目', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%80%E5%8F%B6%E9%9A%9C%E7%9B%AE.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A10Z%2F-1%2F%2F37694ac3981b7c7b99e420d45c71df9df9ee94b591668d57d10aaf307647ffae'],
            ['一帆风顺', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%80%E5%B8%86%E9%A3%8E%E9%A1%BA.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A10Z%2F-1%2F%2Fb370fd619998977892ed0d16d7837ef19f8c90f0d94699fb9fe75e0dc9e3d839'],
            ['愚公移山', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%84%9A%E5%85%AC%E7%A7%BB%E5%B1%B1.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A10Z%2F-1%2F%2F2be71450f4943f638c0e7265dcdf8ceeeb63494bd266f2f58dbc081f409cba0f'],
            ['泰山压顶', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%B3%B0%E5%B1%B1%E5%8E%8B%E9%A1%B6.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A09Z%2F-1%2F%2F1b9967d57803ce0d7a5dfde1b9117bf1de8a0b91135e8976fbf64e47e3c8de24'],
            ['无中生有', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%97%A0%E4%B8%AD%E7%94%9F%E6%9C%89.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A09Z%2F-1%2F%2F38dc35239b2ca4a505517000362589a7961059e66c5e9085005b64af6cf96446'],
            ['卧薪尝胆', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%8D%A7%E8%96%AA%E5%B0%9D%E8%83%86.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A08Z%2F-1%2F%2F2282afa1d638137ad5e725fec21c689f7467fecc5a1c0a320d1900dfa365b0ca'],
            ['身怀六甲', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%BA%AB%E6%80%80%E5%85%AD%E7%94%B2.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A08Z%2F-1%2F%2F169c3f4b6b28d0490050ee484bead0ab997d9714f629de2fb93bfd2b43c841c8'],
            ['全心投入', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A07Z%2F-1%2F%2Fe26b68b78919c68558bf7283c786d39ec63513d6a2c5e9830f103018b4df28fa'],
            ['如雷贯耳', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%A6%82%E9%9B%B7%E8%B4%AF%E8%80%B3.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A07Z%2F-1%2F%2Fa2b9afa9c252a6b219ca27c4391838ddb226b8c5dbf7bb286333ded934a689b0'],
            ['石破天惊', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%9F%B3%E7%A0%B4%E5%A4%A9%E6%83%8A.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A07Z%2F-1%2F%2F08cebc4c0e26f4164ee8f92936724bc50f4c77a144a5efd46c648cc17fe9c105'],
            ['藕断丝连', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%97%95%E6%96%AD%E4%B8%9D%E8%BF%9E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A06Z%2F-1%2F%2F11350141814eb0b864e7969c2f8637952329c7628f8bdfbb81206ed71d4aad8a'],
            ['日行千里', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%97%A5%E8%A1%8C%E5%8D%83%E9%87%8C.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A06Z%2F-1%2F%2F2b7d6454b58201e2f38bb0e6f3331bd8719bd784b4f77438eab4ce8e03056255'],
            ['穷山恶水', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%A9%B7%E5%B1%B1%E6%81%B6%E6%B0%B4.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A06Z%2F-1%2F%2Fd735c4502d9651c037b107052b2fe69f719d411644c5792565e7fc5478701e30'],
            ['门当户对', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%97%A8%E5%BD%93%E6%88%B7%E5%AF%B9.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A05Z%2F-1%2F%2F03c99c341f409ec80f73bc36689720e91617860e5ac1087882d58826bb39a6a1'],
            ['强词夺理', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%BC%BA%E8%AF%8D%E5%A4%BA%E7%90%86.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A05Z%2F-1%2F%2F0348ea1e77c0b8ed99435588fbcccf4e373c0caac2b60a613864a3b754c6278e'],
            ['七窍生烟', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%83%E7%AA%8D%E7%94%9F%E7%83%9F.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A05Z%2F-1%2F%2F6af204314d3cb186919b78cfcb1bc86a566e89db4fe5986f971ecf143629cba7'],
            ['明镜高悬', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%98%8E%E9%95%9C%E9%AB%98%E6%82%AC.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A04Z%2F-1%2F%2F9b1bb4f86f327379e727757d8758db7a5e0ab0b8035f2918b2da3f8f0a716a9b'],
            ['妙语如珠', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%A6%99%E8%AF%AD%E5%A6%82%E7%8F%A0.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A03Z%2F-1%2F%2F03e2faca7986bda6c4c36f29e7076e76e233db796a8873a1d4b0c162ac5d3794'],
            ['目不识丁', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%9B%AE%E4%B8%8D%E8%AF%86%E4%B8%81.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A03Z%2F-1%2F%2Fdc93435ae6e666f0041fdf989867412554a1e3f26c8b7d430d2cc44ea599d590'],
            ['每况日下', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%AF%8F%E5%86%B5%E6%97%A5%E4%B8%8B.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A02Z%2F-1%2F%2F2173c01ce1bf79607048112c86441ffb1e010265a6ff4f31df6da4c1455d47ed'],
            ['近水楼台', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%BF%91%E6%B0%B4%E6%A5%BC%E5%8F%B0.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A01Z%2F-1%2F%2Ff128505899c0cb885c71cef5b83244e9f2f902e8ad32706c7f27566f4b941203'],
            ['苦口婆心', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%8B%A6%E5%8F%A3%E5%A9%86%E5%BF%83.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A01Z%2F-1%2F%2F843d00f449debd8d40f51d3f9416db621950325ea8909e8ef2820c6ea8c0338a'],
            ['马放南山', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%A9%AC%E6%94%BE%E5%8D%97%E5%B1%B1.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A01Z%2F-1%2F%2F1f36c7b4e24e9365e7d1ef5e86a4875841811dae999dfca685ec252372dd3d79'],
            ['劳燕分飞', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%8A%B3%E7%87%95%E5%88%86%E9%A3%9E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A01Z%2F-1%2F%2Ffafffc078e1d596d9f65a1693dac3a0f0253cd4651c3c1102ba5ef598c37dbc7'],
            ['马首是瞻', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%A9%AC%E9%A6%96%E6%98%AF%E7%9E%BB.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A01Z%2F-1%2F%2F38707991e8a8c6cff4d17a1bb6871a62309b44151fd7dbfa377906a9210e36c9'],
            ['弥天大谎', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%BC%A5%E5%A4%A9%E5%A4%A7%E8%B0%8E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-02T05%3A40%3A01Z%2F-1%2F%2F698bb20d73f99ac8dee5ac4d03ef7ef943d1a2d092a495b40401982756b91dc2'],
            ['网开一面', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%BD%91%E5%BC%80%E4%B8%80%E9%9D%A2.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A40Z%2F-1%2F%2F65f13d0995890cd725ca68c6e09ac2117010ca1fda42246d739d48f8472e3d0b'],
            ['鱼贯而入', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%B1%BC%E8%B4%AF%E8%80%8C%E5%85%A5.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A40Z%2F-1%2F%2F416dfe3b1390d287e2b83654731e3ee5ce1cd635bd5e51f403cf2eb43c0dc049'],
            ['四通八达', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%9B%9B%E9%80%9A%E5%85%AB%E8%BE%BE.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A40Z%2F-1%2F%2F8e35ebb8bce220b406f87228d691925f3560b3d68890b391c1bb6fbcf0d343de'],
            ['头重脚轻', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%A4%B4%E9%87%8D%E8%84%9A%E8%BD%BB.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A03Z%2F-1%2F%2F990dac5c84d73b1ffd10b6852e06127e8cd223cbdead6931c90bc245c7010e8e'],
            ['命悬一线', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%91%BD%E6%82%AC%E4%B8%80%E7%BA%BF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A03Z%2F-1%2F%2F179110cdd391107b42d86ea22935c40e5a8ef15bf8a5c7b5949668da1611d6d8'],
            ['鱼目混珠', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%B1%BC%E7%9B%AE%E6%B7%B7%E7%8F%A0.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A03Z%2F-1%2F%2Fecc04e62d956438547bfeb7e95c10a0cf6a0b93eac79ce19c7ecbda1841a3bfa'],
            ['胆大包天', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%83%86%E5%A4%A7%E5%8C%85%E5%A4%A9.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A02Z%2F-1%2F%2F54fd5b3c59c0b7842f25cc4cc607da0b1e6ddf7c0af1923f05668a1067b75680'],
            ['水滴石穿', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%B0%B4%E6%BB%B4%E7%9F%B3%E7%A9%BF.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A02Z%2F-1%2F%2F4ae65c95a1a858ad145f013d2727b9f4acad023b43216cd26859df4855c5f739'],
            ['穷困潦倒', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%A9%B7%E5%9B%B0%E6%BD%A6%E5%80%92.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A02Z%2F-1%2F%2Fd2c02f55c9e2c0ba44cd6e551e193aa4fa67297b59852f7faf3a5b995a781d41'],
            ['破口大骂', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%A0%B4%E5%8F%A3%E5%A4%A7%E9%AA%82.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A01Z%2F-1%2F%2F9f4f681fbf957afea36bb7c9c3a3851202e38cfb7357beb91e32d375bd63db89'],
            ['天外有天', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%A4%A9%E5%A4%96%E6%9C%89%E5%A4%A9.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A01Z%2F-1%2F%2F9b71369cef2194ee7bf5d7d60ec8ecee4e72c05cc490fc503f284193a9a7bfca'],
            ['表里如一', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%A1%A8%E9%87%8C%E5%A6%82%E4%B8%80.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A01Z%2F-1%2F%2F57ab37291ef0ac649a168cd51b1a763bd25485fc7cf0e6e11310ee6eac7dd945'],
            ['杀鸡取卵', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%9D%80%E9%B8%A1%E5%8F%96%E5%8D%B5.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A00Z%2F-1%2F%2F5a09b4ac4093d2a7b3055ed23d63563444e2035404d7e9ee906b82043a33bf53'],
            ['横冲直撞', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%A8%AA%E5%86%B2%E7%9B%B4%E6%92%9E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A00Z%2F-1%2F%2Ff21a9ca27e60df9685c39adefaa4279025dd51546a4b50668a24ebe21655c1b6'],
            ['前赴后继', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%89%8D%E8%B5%B4%E5%90%8E%E7%BB%A7.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A43%3A00Z%2F-1%2F%2F8002a09bf00f43ff3cc03d0cb1048c87b2860bd2e69639d8fd8de65f440ece04'],
            ['对牛谈琴', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%AF%B9%E7%89%9B%E8%B0%88%E7%90%B4.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A59Z%2F-1%2F%2F2fe4c31bbe7bfae9ef32b3eb33da0ee173cc984971702926f5935c57bb543a3c'],
            ['东张西望', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%9C%E5%BC%A0%E8%A5%BF%E6%9C%9B.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A59Z%2F-1%2F%2F36128fd60322e89c097eb81738396d094d8a54b0e2158d2a6dc62f6e9263647e'],
            ['半夜三更', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%89%E6%9B%B4%E5%8D%8A%E5%A4%9C.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A58Z%2F-1%2F%2Feb5ccfc5a7885b83e1ac8f3b433faa27b0429bc1b1a51353e4d1ce8df7ef9f95'],
            ['貌合神离', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%B2%8C%E5%90%88%E7%A5%9E%E7%A6%BB.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A58Z%2F-1%2F%2Fc99f1b142e576d0bb138d40876ab7d7a21846fa0c798d1a42bb741aaa91dd444'],
            ['妙手回春', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%A6%99%E6%89%8B%E5%9B%9E%E6%98%A5.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A57Z%2F-1%2F%2Fd5ec21b347f1e6519aefdb192e522a5161192685acd0ee2acdb30672d51922d4'],
            ['普天同庆', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%99%AE%E5%A4%A9%E5%90%8C%E5%BA%86.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A57Z%2F-1%2F%2Ff6c68dea13959a60f10e7b160fc387addeadf14f6e3f09d8d94a259902911165'],
            ['百川归海', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E7%99%BE%E5%B7%9D%E5%BD%92%E6%B5%B7.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A56Z%2F-1%2F%2Fc9fa52583a7a0cb414c1a7376e1906dafc7e77e4a02d116456849b595cdf20fa'],
            ['指鹿为马', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%8C%87%E9%B9%BF%E4%B8%BA%E9%A9%AC.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A56Z%2F-1%2F%2F32638451da525868c1cd3c625d8571813c57aa94264f83b42be5011da948ffdc'],
            ['掩人耳目', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%8E%A9%E4%BA%BA%E8%80%B3%E7%9B%AE.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A56Z%2F-1%2F%2F2df0918fac649406c729c862abc65ca3fab1bee8da6c115f92ac6aabf83edc86'],
            ['若隐若现', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%8B%A5%E9%9A%90%E8%8B%A5%E7%8E%B0.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A55Z%2F-1%2F%2F9a3df08f4977b14e0e485c54dcdc32a81c30e35d9221cd3a0b1aa519be127ab1'],
            ['弹尽粮绝', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%BC%B9%E5%B0%BD%E7%B2%AE%E7%BB%9D.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A55Z%2F-1%2F%2F5ac82c347359d01464fec333dfe4ae2381c5f4c742637065df4213c60a10825b'],
            ['沧海一粟', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%B2%A7%E6%B5%B7%E4%B8%80%E7%B2%9F.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A55Z%2F-1%2F%2F1ec0c035586cabd24eb30d4f18e03e481cb106e4b58eb66973fc6bd3c72ea12a'],
            ['一目十行', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%80%E7%9B%AE%E5%8D%81%E8%A1%8C.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A54Z%2F-1%2F%2Fba868fcac885e735138cf9549b2c0ac9e65cc2ce7fa9725349965672cab8a32e'],
            ['远走高飞', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%BF%9C%E8%B5%B0%E9%AB%98%E9%A3%9E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A54Z%2F-1%2F%2F47697cd0099cadc60bf8eb13e8febbe4f9e9b8a3fcc394e391516f7e37f13142'],
            ['只手遮天', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%8F%AA%E6%89%8B%E9%81%AE%E5%A4%A9.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A54Z%2F-1%2F%2Feec02b6ac95f73c305123ca6b0d00b60d06ff83df84ac420e7eb3a7cae8eed21'],
            ['坐吃空山', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%9D%90%E5%90%83%E7%A9%BA%E5%B1%B1.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A53Z%2F-1%2F%2F4a3ebadcdab7b836ea258077f7318f9b04e80bfec299cc077883011f24ae4609'],
            ['心直口快', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%BF%83%E7%9B%B4%E5%8F%A3%E5%BF%AB.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A53Z%2F-1%2F%2Fd27f45f69707fc72615bc08152bae1ff12873956e0a61df6d538fc6614df6f44'],
            ['胆小如鼠', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%83%86%E5%B0%8F%E5%A6%82%E9%BC%A0.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A53Z%2F-1%2F%2Fb346e71ffd410ddf50b460ffcd4a482c14840d3e26f2f12349588bd9abaaae28'],
            ['苦中作乐', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E8%8B%A6%E4%B8%AD%E4%BD%9C%E4%B9%90.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A53Z%2F-1%2F%2Fd10a35f32acf8e03504eaa50e1223c76af1e58c2e3b88b68009a4f21bb93a7f5'],
            ['哭笑不得', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%93%AD%E7%AC%91%E4%B8%8D%E5%BE%97.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A52Z%2F-1%2F%2Fb6f536fa0d42397cf55ec8c8009caecbbe8359c67d38e124be2df0847fa0da9e'],
            ['月下老人', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E6%9C%88%E4%B8%8B%E8%80%81%E4%BA%BA.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A51Z%2F-1%2F%2F1e0360f852d59e6d1ec086d93afae025c90d28a755c9ad4dd944bd71c5bb0557'],
            ['偷天换日', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E5%81%B7%E5%A4%A9%E6%8D%A2%E6%97%A5.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A28Z%2F-1%2F%2F5c091b36d8df930ef57a0b2bc055900c156653398bea5478cd93c185a44620d4'],
            ['风花雪月', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E9%A3%8E%E8%8A%B1%E9%9B%AA%E6%9C%88.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A28Z%2F-1%2F%2F20502baca6d694125b5d0b4d702666474a7f0ffd16555cf49d7ed225b3b19e8d'],
            ['人面兽心', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%BA%BA%E9%9D%A2%E5%85%BD%E5%BF%83.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A27Z%2F-1%2F%2F4db4435ac3b284a432c9db8bee06cac1add29065fbd3f8bf61f1ffa2326aa0ef'],
            ['三人成虎', 'http://dbp-resource.gz.bcebos.com/c34fc6ae-3146-0c82-9cee-105b18065f17/%E4%B8%89%E4%BA%BA%E6%88%90%E8%99%8E.png?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-08T02%3A42%3A27Z%2F-1%2F%2F0602fbaf21a33c96a42870fed3e2042c9f157292e48091392dd52943efca6d42']
        ]
        
    def launchRequest(self):
        
        card = TextCard('说出“开始猜成语”即可开始看图猜成语')
        return {
            'card': card,
            'outputSpeech': r'你准备好了吗，我们一起猜成语吧'
        }
        
    
    def quesheng(self):
        
        num = open("num.txt", "w")
        num.write(self.imageurl[self.number][0])
        num.close()
        return {
            'card': TextCard('抱歉，我没有理解您的意思'),
            'outputSpeech': r'抱歉，我没有理解您的意思'
        }
    
    def howlg(self):
        
        lun = open("lun.txt", "r")
        card = TextCard('您现在在第' + lun.read(2)[-2] + '轮' + '第' + lun.read(2)[-1] + '关')
        return {
            'card': card,
            'outputSpeech': '您现在在第' + lun.read(2)[-2] + '轮' + '第' + lun.read(2)[-1] + '关'
        }
    
    def cidiom(self):
        
        num = open("num.txt", "w")
        num.write(self.imageurl[self.number][0])
        num.close()
        lun = open("lun.txt", "a+")
        g = num.read(2)[-1]
        if g > '5':
            g = 0
            l = str(int(num.read(2)[-2]) + 1)
            lun.write(l + str(g))
        else:
            g = g + 1
            l = str(int(num.read(2)[-2]) + 1)
            lun.write(l + str(g))
        lun.close()
        card = ImageCard()
        card.addItem(self.imageurl[self.number][1])
        card.addCueWords('小度小度，我觉得答案是......')
        card.addCueWords('小度小度，（成语答案）')
        card.addCueWords('小度小度，我需要帮助/我不知道答案')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'嗯嗯，继续'
        }
    
    def idiom(self):
        
        num = open("num.txt", "w")
        num.write(self.imageurl[self.number][0])
        num.close()
        lun = open("lun.txt")
        data = lun.read().lun.close()
        if data[-1] > 5:
            l = data[-2]
            a = 0
            lun.write(str(int(l) + 1) + str(a))
        else:
            pass
        lun.close()
        card = ImageCard()
        card.addItem(self.imageurl[self.number][1])
        card.addCueWords('小度小度，我觉得答案是......')
        card.addCueWords('小度小度，（成语答案）')
        card.addCueWords('小度小度，我需要帮助/我不知道答案')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'上官，请您过目'
        }
    
    def welcome(self):
        
        card = StandardCard()
        card.setTitle('看图猜成语引导')
        card.setContent('说出，开始猜成语，或，我准备好了，即可开始看图猜成语')
        card.setContent('想出答案以后：')
        card.setContent('说出：“我认为答案是......”或者“我觉得答案是......”')
        card.setContent('当您真的想不出答案时，说出“我需要帮助”或者“我不知道答案”即可获得提示')
        card.setContent('成语图片由度秘事业部提供')
        card.addCueWords('小度小度，开始猜成语')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'说出，开始猜成语，让我们开始猜成语吧'
        }
        
    def answerunknow(self):
        
        number = random.randint(1,4)
        num = open("num.txt", "r")

        if number == 1:
            
            ra = num.read(4)
            num.close()
            card = TextCard('要加油哦，这一次就告诉你答案吧，答案是' + ra )
            self.waitAnswer()
            return {
                'outputSpeech': r'要加油哦，这一次就告诉你答案吧，答案是' + ra
            }
        elif number == 2:
            ra = num.read(1)
            num.close()
            card = TextCard('上官，答案的第一个字是' + ra)
            self.waitAnswer()
            return {
                'outputSpeech': r'上官，答案的第一个字是' + ra
            }
        elif number == 3:
            ra = num.read(2)
            num.close()
            card = TextCard('皇上，答案的前两个字是' + ra)
            self.waitAnswer()
            return {
                'outputSpeech': r'皇上，答案的前两个字是' + ra
            }
        elif number == 4:
            card = TextCard('诶呀，成语躲起来了，加油想一想吧')
            self.waitAnswer()
            return {
                'outputSpeech': '诶呀，成语躲起来了，加油想一想吧'
            }
                           
    def answeridiom(self):
        
        num = open("num.txt", "r")
        ra = num.read(4)
        num.close()
        answer = self.getSlots('sys.idiom')
        card = ImageCard()
        card.addItem(self.imageurl[self.number][1])
        card.addCueWords('小度小度，我觉得答案是......')
        card.addCueWords('小度小度，我认为答案是......')
        if not answer:
            self.nlu.ask('sys.idiom')
            self.waitAnswer()
            tcard = TextCard('您认为答案是什么呢')
            return {
                'card': tcard,
                'outputSpeech': r'您的答案是什么呢？'
            }
        elif answer ==  ra:
            
            num = open("num.txt", "w")
            lun = open("lun.txt", "r+")
            g = num.read(2)[-1]
            if g > '5':
                g = 0
                l = str(int(num.read(2)[-2]) + 1)
                lun.write(l + str(g))
            else:
                g = g + 1
                l = str(int(num.read(2)[-2]) + 1)
                lun.write(l + str(g))
            num.write(self.imageurl[self.number][0])
            num.close()
            lun.close()
            return {
                'outputSpeech': r'恭喜你答对了，你真棒！再来一道呗',
                'card': card
            }
        else:
            num = open("num.txt", "w")
            lun = open("lun.txt", "r+")
            g = num.read(2)[-1]
            if g > '5':
                g = 0
                l = str(int(num.read(2)[-2]) + 1)
                lun.write(l + str(g))
            else:
                g = g + 1
                l = str(int(num.read(2)[-2]) + 1)
                lun.write(l + str(g))
            num.write(self.imageurl[self.number][0])
            num.close()
            lun.close()
            return {
                'outputSpeech': '好遗憾，答错了，正确答案是：' + ra + '，不要气馁，再来一道',
                'card': card
            }
    
if __name__ == '__main__':
    
    pass
    
