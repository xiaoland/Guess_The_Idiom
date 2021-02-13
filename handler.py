#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# author: xiaoland, sunshaolei
# create_time: 2018/6/1
# description: dueros有屏技能-看图猜成语
#  玩法：
#  - 1、闯关模式，难度递增，错误过多要重来（每个关卡有一定的提示次数）
#  - 2、自由模式，随机抽取，自行结束
#  - 3、新增排行榜
#  - 4、每完成一个成语，就会给出解释
#  - 5、更精美的页面


import random
import json

from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template import ListTemplate1
from dueros.directive.Display.template import ListTemplateItem

from dueros.card.ImageCard import ImageCard
from dueros.card.ListCard import ListCard
from dueros.card.ListCardItem import ListCardItem
from dueros.card.StandardCard import StandardCard
from dueros.card.TextCard import TextCard


from log import Log


class GuessIdiom(Bot):

    def __init__(self, request_data):

        super(GuessIdiom, self).__init__(request_data)
        # fix by sunshaolei 不需要再初始化的时候就随机数，这样每次请求都会重新随机，效率低而且可能随机到重复的(code:random.randint(0:67))
        
        self.idiom_url_list = json.load(open("./data/json/idiom_url_list.json", "r", encoding="utf-8"))
        self.commonly_used_image_url_list = json.load(open("./data/json/commonly_used_image_url_list.json", "r", encoding="utf-8"))
        self.request_data = request_data

        self.log = Log()

        self.log.add_log("Init: New request, initializing...", 1)
        self.wait_answer()

        self.add_launch_handler(self.handle_welcome)
        self.add_intent_handler("welcome", self.welcome)
        self.add_intent_handler("idiom", self.idiom)
        self.add_intent_handler("c_idiom", self.cidiom)
        self.add_intent_handler("howlg", self.howlg)
        self.add_intent_handler("idiom_answer", self.answeridiom)
        self.add_intent_handler("answerunknow", self.answerunknow)
        self.add_intent_handler("answerhelp", self.answerunknow)
        self.add_intent_handler("nidiom", self.nidiom)
        self.add_intent_handler("ai.dueros.common.default_intent", self.quesheng)

    def handle_welcome(self):

        """
        欢迎语
        :return:
        """
        self.log.add_log("handle_welcome: start", 1)
        template = ListTemplate1()
        template.set_token("1")
        template.set_background_image(self.commonly_used_image_url_list["welcome_background"])
        template.set_title("看图猜成语-选择游戏模式")

        mode1 = ListTemplateItem()
        mode2 = ListTemplateItem()
        mode1.set_plain_primary_text('p')
        item.set_plain_secondary_text('s')
        item.set_image('asfasdf')
        listTemplate.add_item(item)

        directive = RenderTemplate(template)
        return {
            "directives": [directive],
            "outputSpeech": r"请选择游戏模式，有不明白的可以像这样问我：小度小度，什么是闯关模式"
        }

    def idiom(self):
        """
        开局，初始化
        :return:
        """

        # ------------- fix by sunshaolei -----不要记文件了，记录session吧

        # num = open("./num.txt", "w")
        # wt = self.idiom_url_list[self.number][0] + "000"
        # print(wt)
        # num.write(wt)
        # num.close()

        # ------------- fix by sunshaolei -------

        pos = random.randint(0, 75)

        self.set_session_attribute("pos", pos, 0)  # 存储当前正在出现的图片的答案
        self.set_session_attribute("error_num", 0, 0)  # 存储当前使用者错误次数
        self.set_session_attribute("guanqia_num", 1, 1)  # 存储当前使用者关卡
        self.set_session_attribute("lun_num", 1, 1)  # 存储当前使用者关卡
        self.set_session_attribute("lerror_num", 0, 3) # 存储轮错误
        card = ImageCard()
        card.addItem(self.idiom_url_list[pos][1])
        card.addCueWords(r"我觉得答案是......")
        card.addCueWords(r"（你的成语答案）")
        card.addCueWords(r"我需要帮助/我不知道答案")
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"上官，请您过目"
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

        pos = int(self.get_session_attribute("pos", 0))

        guanqia_num = int(self.get_session_attribute("guanqia_num", 0))
        lun_num = int(self.get_session_attribute("lun_num", 0))
        error_num = int(self.get_session_attribute("error_num", 0))
        lerror_num = int(self.get_session_attribute("lerror_num", 0))

        result = self.get_slots("idiom")
        try:
            answer = json.loads(result)
            answer = answer.get("origin")
        except:
            answer = result

        print(repr(answer))
        print(repr(self.idiom_url_list[pos][0]))

        if not answer:

            self.nlu.ask("idiom")
            self.wait_answer()
            return {
                "outputSpeech": r"您的答案是什么呢？"
            }
        elif answer == self.idiom_url_list[pos][0]:  # 此分支为回答正确的处理

            # ------fix by susnhaolei ----- 因为没有注释，没太看明白代码这几个字段表示的意思，我理解应该是成功之后记录成功次数吗？（emm，这是关卡与轮数的更新）
            if guanqia_num >= 10:
                self.set_session_attribute("guanqia_num", 1, 0)  # 关卡加一
                self.set_session_attribute("lun_num", lun_num + 1, 0)
                self.set_session_attribute("lerror_num", 0, 0)
                self.set_session_attribute("error_num", 0, 0)
                if error_num == 0:
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        "http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0")
                    bodyTemplate.setPlainTextContent(
                        r"你太棒了，全部都答对了，一共有十道题哦，请对我说"开始下一轮",进入第" + str(int(lun_num) + 1) + "轮，需要退出请说：“退出”。")
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        "directives": [directive],
                        "outputSpeech": r"你太棒了，全部都答对了，说出“开始下一轮"进入第" + str(int(lun_num) + 1) + "轮，如需退出，请说，退出"
                    }
                else:

                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        "http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0")
                    bodyTemplate.setPlainTextContent(r"你太棒了，答对了" + str(10 - error_num) + r"道题目，说出“开始下一轮”即可进入第" + str(
                        int(lun_num) + 1) + "轮，需要退出请说：“退出”。")
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        "directives": [directive],
                        "outputSpeech": r"你太棒了，答对了" + str(10 - error_num) + r"道题目，说出“开始下一轮”即可进入第" + str(
                            int(lun_num) + 1) + "轮，需要退出请说：“退出”。"
                    }

            else:

                pos = random.randint(0, 75)

                self.set_session_attribute("guanqia_num", guanqia_num + 1, 0)  # 关卡加一
                self.set_session_attribute("lun_num", lun_num, 0)
                self.set_session_attribute("pos", pos, 0)
                self.set_session_attribute("lerror_num", 0, 0)

                card = ImageCard()
                card.addItem(self.idiom_url_list[pos][1])
                card.addCueWords(r"我觉得答案是......")
                card.addCueWords(r"我认为答案是......")

                self.wait_answer()
                return {
                    "outputSpeech": r"恭喜你答对了，您已经闯过了第" + str(int(guanqia_num) + 0) + "关，加油！让我们继续吧",
                    "card": card
                }
        else:
            if guanqia_num >= 10:
                self.set_session_attribute("guanqia_num", 1, 0)  # 关卡设为零
                self.set_session_attribute("lun_num", lun_num + 1, 0)  # 轮数加一
                self.set_session_attribute("error_num", 0, 0)
                self.set_session_attribute("lerror_num", 0, 0)
                if lerror_num > 2:
                    bodyTemplate = BodyTemplate1()
                    bodyTemplate.setBackGroundImage(
                        "http://dbp-resource.gz.bcebos.com/509b8811-c1d4-238d-5a0e-1f1b319a9e4b/%E5%85%A8%E5%BF%83%E6%8A%95%E5%85%A5.jpg?authorization=bce-auth-v1%2Fa4d81bbd930c41e6857b989362415714%2F2018-06-27T05%3A30%3A00Z%2F-1%2F%2F65d7fb04d32c2d64abb134ad8be345c4bd81a32bdfe8071dc56d19da7c9de5f0")
                    bodyTemplate.setPlainTextContent(r"这一题的答案是" + self.idiom_url_list[pos][0] + "不过你很棒棒哦，一共十道题，您答对了：" + str(
                        10 - error_num) + r"题，说出“开始下一轮”即可进入第" + str(int(lun_num) + 1) + "轮，需要退出请说：“退出”。")
                    directive = RenderTemplate(bodyTemplate)
                    return {
                        "directives": [directive],
                        "outputSpeech": "这一题的答案是" + self.idiom_url_list[pos][0] + "不过你很棒棒哦，一共十道题，您答对了：" + str(
                            10 - error_num) + r"题，说出"开始下一轮"，即可进入第" + str(int(lun_num) + 1) + "轮，需要退出请说，退出，"
                    }

                else:

                    new_pos = random.randint(0, 75)
                    self.set_session_attribute("pos", new_pos, 0)
                    self.set_session_attribute("lerror_num", 0, 0)
                    card = ImageCard()
                    card.addItem(self.idiom_url_list[new_pos][1])

                    return {
                        "outputSpeech": r"好遗憾，还是答错了，正确答案是：" + self.idiom_url_list[pos][0] + "，不要气馁，让我们继续吧",
                        "card": card
                    }
            else:

                self.set_session_attribute("lun_num", lun_num, 0)  # 轮数不变
                self.wait_answer()
                if lerror_num > 2:
                    self.set_session_attribute("guanqia_num", int(guanqia_num) + 1, 0)  # 关卡加一

                    new_pos = random.randint(0, 75)
                    self.set_session_attribute("pos", new_pos, 0)
                    self.set_session_attribute("lerror_num", 0, 0)
                    self.set_session_attribute("error_num", error_num + 1, 0)

                    card = ImageCard()
                    card.addItem(self.idiom_url_list[new_pos][1])
                    card.addCueWords(r"我觉得答案是......")

                    return {
                        "outputSpeech": r"好遗憾，还是答错了，正确答案是：" + self.idiom_url_list[pos][0] + "，不过您已经闯过了" + str(
                            guanqia_num + 0) + "让我们继续吧",
                        "card": card
                    }
                elif int(lerror_num) < 4:
                    self.set_session_attribute("lerror_num", int(lerror_num) + 1, 0)
                    return {
                        "outputSpeech": r"你已经答错了%d次了，再努力想想吧，需要帮助可以说，我需要帮助" % (lerror_num + 1),
                        "reprompt": r"答错了哦，再努力想想吧，需要帮助可以说，我需要帮助"
                    }

    def quesheng(self):

        error_num = int(self.get_session_attribute("lerror_num", 0))  # 获取错误次数
        self.set_session_attribute("lerror_num", error_num + 1, 0)  # 增加错误次数

        self.wait_answer()
        return {
            "outputSpeech": r"再努力想想吧，需要帮助可以说，我需要帮助",
            "reprompt": r"答错了哦，再努力想想吧，需要帮助可以说，我需要帮助",
        }

    def howlg(self):

        l = int(self.get_session_attribute("lun_num", 0))
        g = int(self.get_session_attribute("guanqia_num", 0))
        card = TextCard(r"您现在在第" + str(l) + r"轮" + r"第" + str(g) + r"关")
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"您现在在第" + str(l) + r"轮" + r"第" + str(g) + r"关"
        }

    def cidiom(self):

        rand_ids = random.randint(0, 75)
        guanqia_num = int(self.get_session_attribute("guanqia_num", 0))
        lun_num = int(self.get_session_attribute("lun_num", 0))
        error_num = int(self.get_session_attribute("error_num", 0))
        pos = self.get_session_attribute("pos", "")

        if guanqia_num > 9:
            self.set_session_attribute("lun_num", lun_num + 1, 0)
            self.set_session_attribute("guanqia_num", 0, 0)
        else:
            self.set_session_attribute("lun_num", lun_num, 0)
            self.set_session_attribute("guanqia_num", guanqia_num + 1, 0)

        self.set_session_attribute("pos", rand_ids, 0)
        self.set_session_attribute("error_num", error_num + 1, 0)
        card = ImageCard()
        card.addItem(self.idiom_url_list[rand_ids][1])
        card.addCueWords("我觉得答案是......")
        card.addCueWords("（你的成语答案）")
        card.addCueWords("我需要帮助/我不知道答案")
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"上一题的答案是" + self.idiom_url_list[int(pos)][0] + "，好的，让我们进入第" + str(guanqia_num + 1) + "题吧"
        }

    def nidiom(self):

        rand_ids = random.randint(0, 75)
        lun_num = int(self.get_session_attribute("lun_num", 0))
        self.set_session_attribute("guanqia_num", 1, 0)
        self.set_session_attribute("error_num", 0, 0)
        self.set_session_attribute("lerror_num", 0, 0)
        self.set_session_attribute("pos", rand_ids, 0)
        card = ImageCard()
        card.addItem(self.idiom_url_list[rand_ids][1])
        card.addCueWords("我觉得答案是......")
        card.addCueWords("（你的成语答案）")
        card.addCueWords("我需要帮助/我不知道答案")
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"好的，让我们进入第" + str(lun_num) + "轮"
        }

    def welcome(self):

        card = StandardCard()
        card.setTitle("看图猜成语引导")
        card.setContent("说出，开始猜成语，或，我准备好了，即可开始看图猜成语")
        card.setContent("想出答案以后：")
        card.setContent("说出：“我认为答案是......”或者“我觉得答案是......”")
        card.setContent("当您真的想不出答案时，说出“我需要帮助”或者“我不知道答案”即可获得提示")
        card.setContent("成语图片由度秘事业部提供")
        card.addCueWords("开始猜成语")
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"说出，开始猜成语，让我们开始猜成语吧"
        }

    def answerunknow(self):
        self.wait_answer()
        number = random.randint(2, 4)
        pos = int(self.get_session_attribute("pos", 0))
        ra = self.idiom_url_list[pos][0]
        if number == 2:
            card = TextCard("上官，答案的第一个字是" + ra[0])
            self.wait_answer()
            return {
                "outputSpeech": r"上官，答案的第一个字是" + ra[0]
            }
        elif number == 3:
            card = TextCard("皇上，答案的前两个字是" + ra[0] + ra[1])
            self.wait_answer()
            return {
                "outputSpeech": r"皇上，答案的前两个字是" + ra[0] + ra[1]
            }
        elif number == 4:
            card = TextCard("诶呀，成语躲起来了，加油想一想吧")
            self.wait_answer()
            return {
                "outputSpeech": r"诶呀，成语躲起来了，加油想一想吧"
            }


if __name__ == "__main__":
    pass

