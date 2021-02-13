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


class IdiomGuessing(Bot):

    def __init__(self, data):

        super().__init__(data)
        # fix by sunshaolei 不需要再初始化的时候就随机数，这样每次请求都会重新随机，效率低而且可能随机到重复的(code:random.randint(0:67))

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

    def launchRequest(self):

        """
        进入
        :return:
        """
        bodyTemplate = BodyTemplate1()
        bodyTemplate.setBackGroundImage(
            'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E7%9B%AE%E4%B8%8D%E8%AF%86%E4%B8%81.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A29%3A48Z%2F-1%2F%2F454b61cd89235a7248857bb018c3927f82b94bb8ba19de6ecc7e318247f5a7b3')
        bodyTemplate.setPlainTextContent(r'准备好了以后，说出“开始猜成语”即可开始游戏。')

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

        pos = random.randint(0, 75)

        self.setSessionAttribute("pos", pos, 0)  # 存储当前正在出现的图片的答案
        self.setSessionAttribute("error_num", 0, 0)  # 存储当前使用者错误次数
        self.setSessionAttribute("guanqia_num", 1, 1)  # 存储当前使用者关卡
        self.setSessionAttribute("lun_num", 1, 1)  # 存储当前使用者关卡
        self.setSessionAttribute("lerror_num", 0, 3) # 存储轮错误
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
        elif answer == self.imageurl[pos][0]:  # 此分支为回答正确的处理

            # ------fix by susnhaolei ----- 因为没有注释，没太看明白代码这几个字段表示的意思，我理解应该是成功之后记录成功次数吗？（emm，这是关卡与轮数的更新）
            if guanqia_num >= 10:
                self.setSessionAttribute("guanqia_num", 1, 0)  # 关卡加一
                self.setSessionAttribute("lun_num", lun_num + 1, 0)
                self.setSessionAttribute("lerror_num", 0, 0)
                self.setSessionAttribute("error_num", 0, 0)
                if error_num == 0:
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0')
                    bodyTemplate.setPlainTextContent(
                        r'你太棒了，全部都答对了，一共有十道题哦，请对我说"开始下一轮",进入第' + str(int(lun_num) + 1) + '轮，需要退出请说：“退出”。')
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': r'你太棒了，全部都答对了，说出“开始下一轮"进入第' + str(int(lun_num) + 1) + '轮，如需退出，请说，退出'
                    }
                else:

                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0')
                    bodyTemplate.setPlainTextContent(r'你太棒了，答对了' + str(10 - error_num) + r'道题目，说出“开始下一轮”即可进入第' + str(
                        int(lun_num) + 1) + '轮，需要退出请说：“退出”。')
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': r'你太棒了，答对了' + str(10 - error_num) + r'道题目，说出“开始下一轮”即可进入第' + str(
                            int(lun_num) + 1) + '轮，需要退出请说：“退出”。'
                    }

            else:

                pos = random.randint(0, 75)

                self.setSessionAttribute("guanqia_num", guanqia_num + 1, 0)  # 关卡加一
                self.setSessionAttribute("lun_num", lun_num, 0)
                self.setSessionAttribute("pos", pos, 0)
                self.setSessionAttribute("lerror_num", 0, 0)

                card = ImageCard()
                card.addItem(self.imageurl[pos][1])
                card.addCueWords(r'我觉得答案是......')
                card.addCueWords(r'我认为答案是......')

                self.waitAnswer()
                return {
                    'outputSpeech': r'恭喜你答对了，您已经闯过了第' + str(int(guanqia_num) + 0) + '关，加油！让我们继续吧',
                    'card': card
                }
        else:
            if guanqia_num >= 10:
                self.setSessionAttribute("guanqia_num", 1, 0)  # 关卡设为零
                self.setSessionAttribute("lun_num", lun_num + 1, 0)  # 轮数加一
                self.setSessionAttribute("error_num", 0, 0)
                self.setSessionAttribute("lerror_num", 0, 0)
                if lerror_num > 2:
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        'http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0')
                    bodyTemplate.setPlainTextContent(r'这一题的答案是' + self.imageurl[pos][0] + '不过你很棒棒哦，一共十道题，您答对了：' + str(
                        10 - error_num) + r'题，说出“开始下一轮”即可进入第' + str(int(lun_num) + 1) + '轮，需要退出请说：“退出”。')
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        'directives': [directive],
                        'outputSpeech': '这一题的答案是' + self.imageurl[pos][0] + '不过你很棒棒哦，一共十道题，您答对了：' + str(
                            10 - error_num) + r'题，说出"开始下一轮"，即可进入第' + str(int(lun_num) + 1) + '轮，需要退出请说，退出，'
                    }

                else:

                    new_pos = random.randint(0, 75)
                    self.setSessionAttribute("pos", new_pos, 0)
                    self.setSessionAttribute("lerror_num", 0, 0)
                    card = ImageCard()
                    card.addItem(self.imageurl[new_pos][1])

                    return {
                        'outputSpeech': r'好遗憾，还是答错了，正确答案是：' + self.imageurl[pos][0] + '，不要气馁，让我们继续吧',
                        'card': card
                    }
            else:

                self.setSessionAttribute("lun_num", lun_num, 0)  # 轮数不变
                self.waitAnswer()
                if lerror_num > 2:
                    self.setSessionAttribute("guanqia_num", int(guanqia_num) + 1, 0)  # 关卡加一

                    new_pos = random.randint(0, 75)
                    self.setSessionAttribute("pos", new_pos, 0)
                    self.setSessionAttribute("lerror_num", 0, 0)
                    self.setSessionAttribute("error_num", error_num + 1, 0)

                    card = ImageCard()
                    card.addItem(self.imageurl[new_pos][1])
                    card.addCueWords(r'我觉得答案是......')

                    return {
                        'outputSpeech': r'好遗憾，还是答错了，正确答案是：' + self.imageurl[pos][0] + '，不过您已经闯过了' + str(
                            guanqia_num + 0) + '让我们继续吧',
                        'card': card
                    }
                elif int(lerror_num) < 4:
                    self.setSessionAttribute("lerror_num", int(lerror_num) + 1, 0)
                    return {
                        'outputSpeech': r'你已经答错了%d次了，再努力想想吧，需要帮助可以说，我需要帮助' % (lerror_num + 1),
                        'reprompt': r'答错了哦，再努力想想吧，需要帮助可以说，我需要帮助'
                    }

    def quesheng(self):

        error_num = int(self.getSessionAttribute("lerror_num", 0))  # 获取错误次数
        self.setSessionAttribute("lerror_num", error_num + 1, 0)  # 增加错误次数

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

        rand_ids = random.randint(0, 75)
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
        self.setSessionAttribute("error_num", error_num + 1, 0)
        card = ImageCard()
        card.addItem(self.imageurl[rand_ids][1])
        card.addCueWords('我觉得答案是......')
        card.addCueWords('（你的成语答案）')
        card.addCueWords('我需要帮助/我不知道答案')
        self.waitAnswer()
        return {
            'card': card,
            'outputSpeech': r'上一题的答案是' + self.imageurl[int(pos)][0] + '，好的，让我们进入第' + str(guanqia_num + 1) + '题吧'
        }

    def nidiom(self):

        rand_ids = random.randint(0, 75)
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
        number = random.randint(2, 4)
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

