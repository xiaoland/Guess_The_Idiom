#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:xiaoland,sunshaolei
# create_time: 2018/6/1

import random
from dueros.Bot import Bot
import json

from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1

from dueros.card.ImageCard import ImageCard 
from dueros.card.ListCard import ListCard
from dueros.card.ListCardItem import ListCardItem
from dueros.card.StandardCard import StandardCard
from dueros.card.TextCard import TextCard

class guess(Bot):
    
    def __init__(self, data):
        
        super().__init__(data)
        #fix by sunshaolei 不需要再初始化的时候就随机数，这样每次请求都会重新随机，效率低而且可能随机到重复的(code:random.randint(0:67))

        self.waitAnswer()

        self.addLaunchHandler(self.launchRequest)
        self.addIntentHandler('welcome', self.welcome)
        self.addIntentHandler('idiom', self.idiom)
        self.addIntentHandler('c_idiom', self.cidiom)
        self.addIntentHandler('howlg', self.howlg)
        self.addIntentHandler('idiom_answer', self.answeridiom)
        self.addIntentHandler('answerunknow', self.answerunknow)
        self.addIntentHandler('answerhelp', self.answerunknow)
        self.addIntentHandler('nidiom', self.nidiom)
        self.addIntentHandler('ai.dueros.common.default_intent', self.quesheng)
        self.imageurl = [
            ['支离破碎', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%94%AF%E7%A6%BB%E7%A0%B4%E7%A2%8E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A55Z%2F-1%2F%2Fb34d00a868a863f4a2f5e5079564082f5fe84fedc985c0460bec7136d26ef0ab'],
            ['重蹈覆辙', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%87%8D%E8%B9%88%E8%A6%86%E8%BE%99.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A57Z%2F-1%2F%2F313be2b8aed3acd3add552259087cbfd44f94433de25b392b8200b8ff6528566'],
            ['一石二鸟', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%80%E7%9F%B3%E4%BA%8C%E9%B8%9F.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A50Z%2F-1%2F%2Fe67712a139d93b7bd0edfd717fbcf5695059157f80762511e49abaa4742ec54d'],
            ['一叶障目', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%80%E5%8F%B6%E9%9A%9C%E7%9B%AE.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A52Z%2F-1%2F%2F8783bf1fc817a358befcb275862d3f5cf2bca5f6fed635f4b21c7b7f8b69358a'],
            ['一帆风顺', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%80%E5%B8%86%E9%A3%8E%E9%A1%BA.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A51Z%2F-1%2F%2F45464eabffbaed1b21d81230b2936ed879ea96c2ddc291f35377c733a881d0b0'],
            ['愚公移山', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%84%9A%E5%85%AC%E7%A7%BB%E5%B1%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A53Z%2F-1%2F%2F4d71823f8a489358ad73627a8151c1e6f7b3e00efecf6c89c9f897ec4c5c4e14'],
            ['泰山压顶', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%B3%B0%E5%B1%B1%E5%8E%8B%E9%A1%B6.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A34Z%2F-1%2F%2F4cc627fa593cae41d2076b47b0677c4c8c22205f43507cae62d8c42628c71ff4'],
            ['无中生有', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%97%A0%E4%B8%AD%E7%94%9F%E6%9C%89.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A47Z%2F-1%2F%2Ff70f4c40a6c811128d471d8b2f0aee0a0147f0739e0960a0ca129ec5fa1081ae'],
            ['卧薪尝胆', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%8D%A7%E8%96%AA%E5%B0%9D%E8%83%86.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A46Z%2F-1%2F%2F2a0d0502972e94ca2f21b7dd905510f04eadb8e14d2054950c0643a1b59f64bf'],
            ['身怀六甲', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%BA%AB%E6%80%80%E5%85%AD%E7%94%B2.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A08Z%2F-1%2F%2Fe013c083b1a7ae4fc6976e8ac79c81c7940a24b9b49e096006475a8867b1d499'],
            ['全心投入', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0'],
            ['如雷贯耳', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A6%82%E9%9B%B7%E8%B4%AF%E8%80%B3.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A02Z%2F-1%2F%2F33bebb1510bcc9c083a92794702178f332ff48ce0a19c228d66addd70e4455c5'],
            ['石破天惊', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%9F%B3%E7%A0%B4%E6%83%8A%E5%A4%A9.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A09Z%2F-1%2F%2Fff8964f3787e469bfc0434014390ef0fc3bb475a7475a52d031b199d70f178b5'],
            ['藕断丝连', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%97%95%E6%96%AD%E4%B8%9D%E8%BF%9E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A51Z%2F-1%2F%2Fa60f9582583b2fbd045bf10b0de287ffddc568517d57e23cd2c236187967c9d2'],
            ['日行千里', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%97%A5%E8%A1%8C%E5%8D%83%E9%87%8C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F3548d8a22b50905dff53299a5b802fc28183ae3ad244bde511623a565d8b492e'],
            ['穷山恶水', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%A9%B7%E5%B1%B1%E6%81%B6%E6%B0%B4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A59Z%2F-1%2F%2F5f30303f479e209a08cb3a6f7505fa692444d1d74a76cde2bb9a51f3d7a1ae41'],
            ['门当户对', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%97%A8%E5%BD%93%E6%88%B7%E5%AF%B9.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A17Z%2F-1%2F%2F4a12b2e71e38580132e50c6f7e60ce39ee4e7226693872222fa18b6208fe4295'],
            ['强词夺理', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%BC%BA%E8%AF%8D%E5%A4%BA%E7%90%86.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A56Z%2F-1%2F%2F2fbf78d7f514d7c8631b96268111131249e061daf91966a693a77605b606ddf6'],
            ['七窍生烟', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%83%E7%AA%8D%E7%94%9F%E7%83%9F.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A54Z%2F-1%2F%2Fea42310ed43a139fe8baeb108b90c768767ca1e153fa65e9e9f084f46bdf0e35'],
            ['明镜高悬', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%98%8E%E9%95%9C%E9%AB%98%E6%82%AC.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A47Z%2F-1%2F%2Fac824816d9538ee7e75d84090a0d9688f6c78f1ff56f72e39851c3a8335796c3'],
            ['妙语如珠', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A6%99%E8%AF%AD%E5%A6%82%E7%8F%A0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A46Z%2F-1%2F%2Feb2f5f8846de8803d4366d04f8f720556ba5f25d540d1f8ddd2ec62b73036ad6'],
            ['目不识丁', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%9B%AE%E4%B8%8D%E8%AF%86%E4%B8%81.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A48Z%2F-1%2F%2F454b61cd89235a7248857bb018c3927f82b94bb8ba19de6ecc7e318247f5a7b3'],
            ['水滴石穿', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%B0%B4%E6%BB%B4%E7%A9%BF%E7%9F%B3.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A09Z%2F-1%2F%2F41b47a10fd77a95ff0403b90dc018e6b519623f84183e76de087518ae370bcad'],
            ['穷困潦倒', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%A9%B7%E5%9B%B0%E6%BD%A6%E5%80%92.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A55Z%2F-1%2F%2Ff1b6090bebac853513d43f7632b55c13f6e7cf75fbe8a8d4d29a065daff6508e'],
            ['破口大骂', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%A0%B4%E5%8F%A3%E5%A4%A7%E9%AA%82.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A51Z%2F-1%2F%2F0e0eb242713965db213344402015c6a49bef9d16ddd03a540fa7fab859e07701'],
            ['天外有天', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A4%A9%E5%A4%96%E6%9C%89%E5%A4%A9.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A33Z%2F-1%2F%2Fe22e790e3cf25550a93f7a78cc1bfd257c12b8bc1442edac9546055b7ca07797'],
            ['表里如一', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%A1%A8%E9%87%8C%E5%A6%82%E4%B8%80.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A12Z%2F-1%2F%2Fba70cfca1477e9d77f3a73c43e3ed4a647b7cecf68859d0e6370ef2dc0b89d22'],
            ['杀鸡取卵', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%9D%80%E9%B8%A1%E5%8F%96%E5%8D%B5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A07Z%2F-1%2F%2F2c674d176675072db9dfede60d6d316822743b3a2aa6773a598c902fe5e433f8'],
            ['横冲直撞', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%A8%AA%E5%86%B2%E7%9B%B4%E6%92%9E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A02Z%2F-1%2F%2Fdd7f7b6f5456f85602b63b515d5badf171280dd2fe2c49ae3c0db19bf27dafb0'],
            ['前赴后继', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%89%8D%E4%BB%86%E5%90%8E%E7%BB%A7.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A52Z%2F-1%2F%2F8caba59d3f424f80d8b87546d4bc85213160b9423b9efa758cd6b6b10aa56e5a'],
            ['对牛谈琴', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%AF%B9%E7%89%9B%E5%BC%B9%E7%90%B4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A17%3A06Z%2F-1%2F%2Fd602b8077505b0505532d48c13e8a07ef16d842fa62a94c58b13c3dab5cac852'],
            ['东张西望', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%9C%E5%BC%A0%E8%A5%BF%E6%9C%9B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A17%3A06Z%2F-1%2F%2F268f83d06ef15b74cf1b58ea0ccd42a0d34530af366f71d4e2c28bacbfd96db9'],
            ['半夜三更', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%89%E6%9B%B4%E5%8D%8A%E5%A4%9C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A06Z%2F-1%2F%2F585b84a3a6b87acf3356c66c989432280280d0d775b8fed92525b6423e393dc4'],
            ['貌合神离', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%B2%8C%E5%90%88%E7%A5%9E%E7%A6%BB.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A16Z%2F-1%2F%2F4c1b277a9f8db9628c24b50ba976ee897ae9f9df3d02c3744d7eeb8e7cba6bc4'],
            ['妙手回春', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A6%99%E6%89%8B%E5%9B%9E%E6%98%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A47Z%2F-1%2F%2F305ece93407ee90b36c652e9ce3cc5bc86e062951e6e00124e1ffe317f95f9ef'],
            ['普天同庆', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%99%AE%E5%A4%A9%E5%90%8C%E5%BA%86.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A52Z%2F-1%2F%2F2a7775e0a7e4948007fd06de74b23b95f0e902e77795f42d3d132a1820071e68'],
            ['百川归海', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%99%BE%E5%B7%9D%E5%BD%92%E6%B5%B7.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A08Z%2F-1%2F%2Fb256b0b52b5c47800b040cf022e16735934fc40fbdfae00aa7d69724fe54f44b'],
            ['指鹿为马', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%8C%87%E9%B9%BF%E4%B8%BA%E9%A9%AC.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A55Z%2F-1%2F%2Fb5726b4a2ff723d9a7e353a60b069c19481120f0032f88c79777f70eb5190838'],
            ['掩人耳目', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%8E%A9%E4%BA%BA%E8%80%B3%E7%9B%AE.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A48Z%2F-1%2F%2Faddd58c39603076ea60d73de6e08b682b9e6462a94d1e202697b9fff73741b53'],
            ['若隐若现', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%8B%A5%E9%9A%90%E8%8B%A5%E7%8E%B0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A05Z%2F-1%2F%2F023d110931b935b1311bfd846d8494866cf159c726aaabb669bd4f903fa0bb39'],
            ['弹尽粮绝', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%BC%B9%E5%B0%BD%E7%B2%AE%E7%BB%9D.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A28Z%2F-1%2F%2Fefc3e0ffcd7b86f06099e5a0b928baddc7bd9938ad08da45a916791e5cd4e665'],
            ['沧海一粟', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%B2%A7%E6%B5%B7%E4%B8%80%E7%B2%9F.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A14Z%2F-1%2F%2Feda993f9eedf385d94dcb67f8719ff51e375e153f7ea5af3ed31b39a29a4cf98'],
            ['一目十行', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%80%E7%9B%AE%E5%8D%81%E8%A1%8C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A49Z%2F-1%2F%2F63cb1996c32fa54b72add290c718e5e11ce4c7fe1a3b3adefc5ff2cdbd5cdd54'],
            ['只手遮天', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%8F%AA%E6%89%8B%E9%81%AE%E5%A4%A9.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A54Z%2F-1%2F%2F8d587d062352728df5e210e3f0a3ad7e391ae66221bdc02ba41f81504152bcc0'],
            ['坐吃空山', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%9D%90%E5%90%83%E5%B1%B1%E7%A9%BA.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A57Z%2F-1%2F%2F8a83010d48f201c71b1049e02b5b145ae13fefba0244f197ac2ce8ccafbf4349'],
            ['心直口快', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%BF%83%E7%9B%B4%E5%8F%A3%E5%BF%AB.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A47Z%2F-1%2F%2Fce3334dec0e828fbcab4cee988526635173a303edf36dc2679083058508bb89a'],
            ['胆小如鼠', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%83%86%E5%B0%8F%E5%A6%82%E9%BC%A0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A28Z%2F-1%2F%2F435e9ecb7970bec11531281936a48e7897af1befb0a894d8e717ecf7e2030c9f'],
            ['苦中作乐', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%8B%A6%E4%B8%AD%E4%BD%9C%E4%B9%90.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A13Z%2F-1%2F%2Fb73fd04b28805e99db229eeb91f2130a45a8c9c4f79f41462f1fe8938a4b3483'],
            ['哭笑不得', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%93%AD%E7%AC%91%E4%B8%8D%E5%BE%97.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A15Z%2F-1%2F%2F91772dd6a11c84f506ec0169550203c758c7fd7fd9838d4a5cccf633cab513f1'],
            ['月下老人', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%9C%88%E4%B8%8B%E8%80%81%E4%BA%BA.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A53Z%2F-1%2F%2Fe7584c78a66ebf52f00e948ce47aed1e1833ed36acf8ccf1c809284b984b428c'],
            ['偷天换日', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%81%B7%E5%A4%A9%E6%8D%A2%E6%97%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A31%3A04Z%2F-1%2F%2F5b9f8ae395d6f7b8b8c4dfda332bc06df0c7f5d47ebe1a62dad43b14ff8bfd08'],
            ['风花雪月', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%A3%8E%E8%8A%B1%E9%9B%AA%E6%9C%88.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A18%3A08Z%2F-1%2F%2F16e8c21f44c3f14e7ace332a3ab41e751aa9bda08c4975f25b01c3ea3149f56a'],
            ['人面兽心', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%BA%BA%E9%9D%A2%E5%85%BD%E5%BF%83.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2Fee9c92e2acb249edfd21f6c93555e63eec6564f89dcc0bd7bba3d3629f087a14'],
            ['三人成虎', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%89%E4%BA%BA%E6%88%90%E8%99%8E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A06Z%2F-1%2F%2Fb67a6ad11f345721ba44889a54e9f8ca66553828e1b8b4b0a74f50f86eecd98f'],
            ['远走高飞', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%BF%9C%E8%B5%B0%E9%AB%98%E9%A3%9E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A52Z%2F-1%2F%2Ff4914bde23154be4cb06384e58d90a20fcc8a33c7febefa72eae5ed0b3f3ec0f'],
            ['鱼贯而入', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%B1%BC%E8%B4%AF%E8%80%8C%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A51Z%2F-1%2F%2F676f881a59e6289786e28e69831710821978ccfc7406084559ea7e7af400ea3e'],
            ['鱼目混珠', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%B1%BC%E7%9B%AE%E6%B7%B7%E7%8F%A0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A32%3A51Z%2F-1%2F%2F9ddf163a079c78de442ce912b8f0f76ba854d2bb1d31def317b92348cd7a34e4'],
            ['如坐针毡', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A6%82%E5%9D%90%E9%92%88%E6%AF%A1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A05Z%2F-1%2F%2Fbd8284477c4643152b086a929b2a1fc1692d0731f80748e73239c3050717c4c8'],
            ['日上三竿', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%97%A5%E4%B8%8A%E4%B8%89%E7%AB%BF.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A01Z%2F-1%2F%2Feaf21f7ee5637d36cff6e6636a2b9f163602c322a8c5cc8bf348350787efaa72'],
            ['青黄不接', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%9D%92%E9%BB%84%E4%B8%8D%E6%8E%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A55Z%2F-1%2F%2F4a5d6e341a421743125de239c8047b132e7e831158eff132db642064828d14fb'],
            ['逆流而上', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%80%86%E6%B5%81%E8%80%8C%E4%B8%8A.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A48Z%2F-1%2F%2Fd2264cddce9aeba607142fd3011e6a09435687fb08c8ce1ff00bdbb1985aa0c3'],
            ['军令如山', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%86%9B%E4%BB%A4%E5%A6%82%E5%B1%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A13Z%2F-1%2F%2F5c0948f070e42fb39cb562e66a3c4cbefc294276bc93e99971487f9d10a8c808'],
            ['开门见山', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%BC%80%E9%97%A8%E8%A7%81%E5%B1%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A12Z%2F-1%2F%2F53f576de23c7f08517d80ed871ad5bb0359cf3df0d11a1c316d7981c81fb2373'],
            ['火烧眉毛', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%81%AB%E7%83%A7%E7%9C%89%E6%AF%9B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A11Z%2F-1%2F%2F6cb2ddd37859b2819279b7c5b4b88ebd7eeed9d8e7c07472ffd0a7e63b8544f1'],
            ['近水楼台', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%BF%91%E6%B0%B4%E6%A5%BC%E5%8F%B0.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A11Z%2F-1%2F%2F21872fb5953115cffc2374f262312d443f827aafe9b9ee7a475721ca3e637220'],
            ['鸡犬升天', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%B8%A1%E7%8A%AC%E5%8D%87%E5%A4%A9.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A11Z%2F-1%2F%2Ff98f448465c3ef944c248c4525c9a7c3812d86cf1c290d7f5cb52d6ce9c39757'],
            ['话中有话', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E8%AF%9D%E4%B8%AD%E6%9C%89%E8%AF%9D.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A10Z%2F-1%2F%2F4c240a15443d078fc13c79d60fa54c406fb5e7451c1dcc233acde372c1ffc2f4'],
            ['画龙点睛', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%94%BB%E9%BE%99%E7%82%B9%E7%9D%9B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A10Z%2F-1%2F%2Fb3fbda6f39588cb25fcb04acde32199cb950c20b2d554b113d515c958307194c'],
            ['厚此薄彼', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%8E%9A%E6%AD%A4%E8%96%84%E5%BD%BC.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A09Z%2F-1%2F%2F34304ee1e28247e20f631fe492dff7aac71b94a3491e42f60b57ac07a940253b'],
            ['狗急跳墙', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%8B%97%E6%80%A5%E8%B7%B3%E5%A2%99.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A19%3A10Z%2F-1%2F%2F5034628cd1109790fafa252075ce7f1b2e251c33f77a67bb20d83e47783e795d'],
            ['官官相护', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%AE%98%E5%AE%98%E7%9B%B8%E6%8A%A4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A19%3A08Z%2F-1%2F%2F09983161bb316ba1fe8098f3ec1e905e59bfb0cd3abc31acee5dd973e38842a4'],
            ['隔岸观火', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%9A%94%E5%B2%B8%E8%A7%82%E7%81%AB.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A18%3A41Z%2F-1%2F%2F97c040a2a82e2fea7cde846bf7006e2dcbdf0a7534fb887e9394caa102e1f2ba'],
            ['废话连篇', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%BA%9F%E8%AF%9D%E8%BF%9E%E7%AF%87.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A18%3A08Z%2F-1%2F%2Fac9f97cc43e86adbff92fd60ff15e3e4dd2fedda669548604e9540bc9b8ffaa6'],
            ['飞黄腾达', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E9%A3%9E%E9%BB%84%E8%85%BE%E8%BE%BE.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A17%3A52Z%2F-1%2F%2F8663cb4ba342405d2d4a1370204d45ada555b74d5eea69c368ce29331a44cd05'],
            ['半壁江山', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%8D%8A%E5%A3%81%E6%B1%9F%E5%B1%B1.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A14Z%2F-1%2F%2Ffc8c49911bedc5adf814e57bb38a5342fc7c94d303555735878798629d9d19d0'],
            ['八面来风', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%AB%E9%9D%A2%E6%9D%A5%E9%A3%8E.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A09Z%2F-1%2F%2Fb48665ddc3e0fd00062cb0b20d932a1ab1a13054eb5f4b32c4443862fb5eceab'],
            ['百里挑一', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%99%BE%E9%87%8C%E6%8C%91%E4%B8%80.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A11Z%2F-1%2F%2Fed5e0e6d3d42ac90aa31f83b9ec9da7f2a6c16da95acdb8e23623e4bd7e7a73b'],
            ['不分彼此', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E4%B8%8D%E5%88%86%E5%BD%BC%E6%AD%A4.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A14Z%2F-1%2F%2F01f8f87d438c2b1503836e1e769cd01af99b1500afbaf46a47b8543bbf52c401'],
            ['成王败寇', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%88%90%E7%8E%8B%E8%B4%A5%E5%AF%87.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A17Z%2F-1%2F%2F4fc85c0e2468c760841f3a6c5dad44486a17c8a10e57c9f0a08d67f6e5eb6341'],
            ['粗茶淡饭', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%B2%97%E8%8C%B6%E6%B7%A1%E9%A5%AD.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A18Z%2F-1%2F%2F160873ba70c0e166d2ad11997e9096642a87f2ab5cd84195d52cdcfc84570d54'],
            ['安然无恙', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%AE%89%E7%84%B6%E6%97%A0%E6%A0%B7.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A09Z%2F-1%2F%2F78a0f727c7071c696cf7dfa90fce8cc0091e37f6b8610cf2bef0baf64f91012c'],
            ['大显身手', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A4%A7%E6%98%BE%E8%BA%AB%E6%89%8B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A19Z%2F-1%2F%2F7de6117e1d6d9ecc2eb382fb2617ddbe7162f5bb9a150f0ecd9ff404b603e71e'],
            ['单枪匹马', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%8D%95%E6%9E%AA%E5%8C%B9%E9%A9%AC.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A21Z%2F-1%2F%2F5c09472e857c985d4c248dc34d5bef947ca6aad9d58676fb9459f2dfe05d9cf9'],
            ['德高望重', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%BE%B7%E9%AB%98%E6%9C%9B%E9%87%8D.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A48Z%2F-1%2F%2F4ee7fda0f622fbfe8166f9ab226578f29023a1d3c6b1ddbff593ce8705dac3f0'],
            ['大跌眼镜', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%A4%A7%E8%B7%8C%E7%9C%BC%E9%95%9C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A21Z%2F-1%2F%2F704c9f4a0c16b64117dacc2b343ce0dfe85159008016105743fbced16eb132ae'],
            ['楚河汉界', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%A5%9A%E6%B1%89%E6%B2%B3%E7%95%8C.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A19Z%2F-1%2F%2Fcf58a296afbd0bb1e0ad0076cb6476701d8ba9a9a06bad407abf573ebf9fca92'],
            ['朝三暮四', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E6%9C%9D%E4%B8%89%E6%9A%AE%E5%9B%9B.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A16Z%2F-1%2F%2F73075286eac90e9e66a1b9b36a2bfb6301dae9bdbcf4f6173a567b3ddac10f24'],
            ['嫦娥奔月', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%AB%A6%E5%A8%A5%E5%A5%94%E6%9C%88.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A16%3A15Z%2F-1%2F%2F5400d4ae0070c9472aa79102b2b494eb3cdcaaaac1451efb465315c0cc09535b'],
            ['绝处逢生', 'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%BB%9D%E5%A4%84%E9%80%A2%E7%94%9F.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-26T15%3A20%3A11Z%2F-1%2F%2Fedb62519bbd9758e9008f7d89c145f5e1e54a955a0c33d11a73cc4db45e27acd']
        ]
        
    def launchRequest(self):
        """
        进入
        :return:
        """
        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%9B%AE%E4%B8%8D%E8%AF%86%E4%B8%81.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A48Z%2F-1%2F%2F454b61cd89235a7248857bb018c3927f82b94bb8ba19de6ecc7e318247f5a7b3')
        bodyTemplate.setPlainTextContent(r'准备好了以后，说出“开始猜成语”即可开始游戏')


        directive = RenderTemplate(bodyTemplate)
        return {
            'directives': [directive],
            'outputSpeech': r'准备好了了以后，说出，开始猜成语，即可开始游戏'
        }


    def idiom(self):
        """
        开局，初始化
        :return:
        """

        # ------------- fix by sunshaolei -----不要记文件了，记录session吧

        # num = open("./num.txt", "w")
        # wt = self.imageurl[self.number][0] + '000'
        # print(wt)
        # num.write(wt)
        # num.close()

        # ------------- fix by sunshaolei -------

        pos = random.randint(0,87)
        
        self.setSessionAttribute("pos", pos, 0)  # 存储当前正在出现的图片的答案
        self.setSessionAttribute("error_num", 0, 0)  # 存储当前使用者错误次数
        self.setSessionAttribute("guanqia_num", 1, 0)  # 存储当前使用者关卡
        self.setSessionAttribute("lun_num", 0, 0)  # 存储当前使用者关卡
        self.setSessionAttribute("lerror_num", 0, 3)
        card = ImageCard()
        card.addItem(self.imageurl[pos][1])
        card.addCueWords(r'我觉得答案是......')
        card.addCueWords(r'（你的成语答案）')
        card.addCueWords(r'我需要帮助/我不知道答案')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'上官，请您过目'
        }


    def answeridiom(self):
        """
        回答，  建议函数名字和意图名字一致 这样方便查找
        :return:
        """

        # -----fix by sunshaolei------

        # num = open("./num.txt", "r")
        # ra = num.read(4)
        # gs = num.read(7)
        # c = gs[-1]
        # g = gs[-2]
        # l = gs[-3]

        # -----fix by sunshaolei------

        pos = int(self.getSessionAttribute("pos", 0))


        guanqia_num = int(self.getSessionAttribute("guanqia_num", 0))
        lun_num = int(self.getSessionAttribute("lun_num", 0))
        error_num = int(self.getSessionAttribute("error_num", 0))
        lerror_num = int(self.getSessionAttribute("lerror_num", 0))

        result = self.getSlots('idiom')
        try:
            answer = json.loads(result)
            answer = answer.get("origin")
        except:
            answer = result

        print(repr(answer))
        print(repr(self.imageurl[pos][0]))

        if not answer:

            self.nlu.ask('idiom')
            self.waitAnswer()
            return {
                'outputSpeech': r'您的答案是什么呢？'
            }
        elif answer == self.imageurl[pos][0]:      # 此分支为回答正确的处理


            # ------fix by susnhaolei ----- 因为没有注释，没太看明白代码这几个字段表示的意思，我理解应该是成功之后记录成功次数吗？（emm，这是关卡与轮数的更新）
            if guanqia_num >= 9:
                self.setSessionAttribute("guanqia_num", 0, 0)    # 关卡加一
                self.setSessionAttribute("lun_num", lun_num + 1, 0)
                self.setSessionAttribute("lerror_num", 0, 0)
                self.setSessionAttribute("error_num", 0, 0)
                if error_num == 0:
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0')
                    bodyTemplate.setPlainTextContent(r'你太棒了，全部都答对了，一共有十道题哦，说出“下一轮”即可进入第' + str(int(lun_num) + 1) + '轮，需要退出请说：“退出”。')
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': r'你太棒了，全部都答对了，说出“下一轮”即可进入第' + str(int(lun_num) + 1) + '轮，如需退出，请说，退出'
                    }
                else:
                
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0')
                    bodyTemplate.setPlainTextContent(r'你太棒了，答对了' + str(10 - error_num) + r'道题目，说出“下一轮”即可进入第' + str(lun_num + 1) + '轮，需要退出请说：“退出”。')
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': r'你太棒了，全部都答对了，说出“下一轮”即可进入第' + str(int(lun_num) + 1) + '轮，如需退出，请说，退出'
                    }

            else:

                pos = random.randint(0, 87)

                self.setSessionAttribute("guanqia_num", guanqia_num + 1, 0)    # 关卡加一
                self.setSessionAttribute("lun_num", lun_num, 0)
                self.setSessionAttribute("pos", pos, 0)
                self.setSessionAttribute("lerror_num", 0, 0)
                guanqia_num = self.getSessionAttribute("guanqia_num", 0)

                card = ImageCard()
                card.addItem(self.imageurl[pos][1])
                card.addCueWords(r'我觉得答案是......')
                card.addCueWords(r'我认为答案是......')

                self.waitAnswer()
                return {
                    'outputSpeech': r'恭喜你答对了，您已经闯到了第' + str(int(guanqia_num) + 0) + '关，加油！让我们继续吧',
                    'card': card
                }
        else:            
            if guanqia_num >= 10:
                self.setSessionAttribute("guanqia_num", 0, 0)  # 关卡设为零
                self.setSessionAttribute("lun_num", lun_num + 1, 0) # 轮数加一
                self.setSessionAttribute("error_num",  0, 0)
                self.setSessionAttribute("lerror_num",  0, 0)
                if lerror_num > 2:
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage('http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0')
                    bodyTemplate.setPlainTextContent(r'这一题的答案是' + self.imageurl[pos][0] + '不过你很棒棒哦，一共十道题，您答对了：' + str(10 - error_num) + r'题，说出“下一轮”即可进入第' + str(int(lun_num) + 1) + '轮，需要退出请说：“退出”。')
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': '这一题的答案是' + self.imageurl[pos][0] + '不过你很棒棒哦，一共十道题，您答对了：' + str(10 - error_num) + r'题，说出，下一轮，即可进入第' + str(int(lun_num) + 1) + '轮，需要退出请说，退出，'
                    }
                    
                else:
                    
                    new_pos = random.randint(0, 87)
                    self.setSessionAttribute("pos", new_pos, 0)
                    self.setSessionAttribute("lerror_num", 0, 0)
                    card = ImageCard()
                    card.addItem(self.imageurl[new_pos][1])

                    return {
                        'outputSpeech': r'好遗憾，还是答错了，正确答案是：' + self.imageurl[pos][0] + '，不要气馁，让我们继续吧',
                        'card': card
                    }
            else:

                self.setSessionAttribute("lun_num", lun_num, 0)  #轮数不变
                self.waitAnswer()
                if lerror_num > 2:
                    self.setSessionAttribute("guanqia_num", int(guanqia_num) + 1, 0)  # 关卡加一

                    new_pos = random.randint(0, 87)
                    self.setSessionAttribute("pos", new_pos, 0)
                    self.setSessionAttribute("lerror_num", 0, 0)
                    self.setSessionAttribute("error_num", error_num + 1, 0)

                    card = ImageCard()
                    card.addItem(self.imageurl[new_pos][1])
                    card.addCueWords(r'我觉得答案是......')

                    return {
                        'outputSpeech': r'好遗憾，还是答错了，正确答案是：' + self.imageurl[pos][0] + '，不过您已经闯到了' + str(guanqia_num - 1) + '让我们继续吧',
                        'card': card
                    }
                elif int(lerror_num) < 4:
                    self.setSessionAttribute("lerror_num", int(lerror_num) + 1, 0)
                    return {
                        'outputSpeech': r'你已经答错了%d次了，再努力想想吧，需要帮助可以说，我需要帮助' % (lerror_num + 1),
                        'reprompt': r'答错了哦，再努力想想吧，需要帮助可以说，我需要帮助'
                    }


    def quesheng(self):

        error_num = int(self.getSessionAttribute("lerror_num", 0))    # 获取错误次数
        self.setSessionAttribute("lerror_num", error_num + 1, 0)   # 增加错误次数

        self.waitAnswer()
        return {
            'outputSpeech': r'再努力想想吧，需要帮助可以说，我需要帮助',
            'reprompt': r'答错了哦，再努力想想吧，需要帮助可以说，我需要帮助',
        }
    
    def howlg(self):
        
        l = int(self.getSessionAttribute("lun_num", 0))
        g = int(self.getSessionAttribute("guanqia_num", 0))
        card = TextCard(r'您现在在第' + str(l) + r'轮' + r'第' + str(g) + r'关')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'您现在在第' + str(l) + r'轮' + r'第' + str(g) + r'关'
        }
    
    def cidiom(self):
        
        rand_ids = random.randint(0,87)
        guanqia_num = int(self.getSessionAttribute("guanqia_num", 0))
        lun_num = int(self.getSessionAttribute("lun_num", 0))
        error_num = int(self.getSessionAttribute("error_num", 0))
        pos = self.getSessionAttribute("pos", '')
        
        if guanqia_num > 9:
            self.setSessionAttribute("lun_num", lun_num + 1, 0)
            self.setSessionAttribute("guanqia_num", 0, 0)
        else:
            self.setSessionAttribute("lun_num", lun_num, 0)
            self.setSessionAttribute("guanqia_num", guanqia_num + 1, 0)
        
        self.setSessionAttribute("pos", rand_ids, 0)
        card = ImageCard()
        card.addItem(self.imageurl[rand_ids][1])
        card.addCueWords('我觉得答案是......')
        card.addCueWords('（你的成语答案）')
        card.addCueWords('我需要帮助/我不知道答案')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'上一题的答案是' + self.imageurl[int(pos)][0] + '，好的，让我们继续吧'
        }
    
    def nidiom(self):
        
        rand_ids = random.randint(0,87)
        lun_num = int(self.getSessionAttribute("lun_num", 0))
        self.setSessionAttribute("guanqia_num", 1, 0)
        self.setSessionAttribute("error_num", 0, 0)
        self.setSessionAttribute("lerror_num", 0, 0)
        self.setSessionAttribute("pos", rand_ids, 0)
        card = ImageCard()
        card.addItem(self.imageurl[rand_ids][1])
        card.addCueWords('我觉得答案是......')
        card.addCueWords('（你的成语答案）')
        card.addCueWords('我需要帮助/我不知道答案')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'好的，让我们进入第' + str(lun_num) + '轮'
        }
    
    def welcome(self):
        
        card = StandardCard()
        card.setTitle('看图猜成语引导')
        card.setContent('说出，开始猜成语，或，我准备好了，即可开始看图猜成语')
        card.setContent('想出答案以后：')
        card.setContent('说出：“我认为答案是......”或者“我觉得答案是......”')
        card.setContent('当您真的想不出答案时，说出“我需要帮助”或者“我不知道答案”即可获得提示')
        card.setContent('成语图片由度秘事业部提供')
        card.addCueWords('开始猜成语')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'说出，开始猜成语，让我们开始猜成语吧'
        }
        
    def answerunknow(self):
        self.waitAnswer()
        number = random.randint(2,4)
        pos = int(self.getSessionAttribute("pos", 0))
        ra = self.imageurl[pos][0]
        if number == 2:
            card = TextCard('上官，答案的第一个字是' + ra[0])
            self.waitAnswer()
            return {
                'outputSpeech': r'上官，答案的第一个字是' + ra[0]
            }
        elif number == 3:
            card = TextCard('皇上，答案的前两个字是' + ra[0] + ra[1])
            self.waitAnswer()
            return {
                'outputSpeech': r'皇上，答案的前两个字是' + ra[0] + ra[1]
            }
        elif number == 4:
            card = TextCard('诶呀，成语躲起来了，加油想一想吧')
            self.waitAnswer()
            return {
                'outputSpeech': r'诶呀，成语躲起来了，加油想一想吧'
            }
                           

if __name__ == '__main__':
    
    pass
    
