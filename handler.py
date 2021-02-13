#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# author: xiaoland, sunshaolei
# create_time: 2018/6/1
# description: dueros有屏技能-看图猜成语
#  玩法：
#  - 1、闯关模式，难度递增，错误过多要重来（每个关卡有一定的提示次数）「难度递增在2021.2.13更新中没有进行」
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
        self.add_intent_handler("entry_mode", self.handle_entry_mode)
        self.add_intent_handler("free_mode", self.handle_free_mode)
        self.add_intent_handler("entry_mode_ranking", self.handle_entry_mode_ranking)
        self.add_intent_handler("skip", self.handle_skip)
        self.add_intent_handler("now_status", self.handle_now_status)
        self.add_intent_handler("answer_idiom", self.handle_answer)
        self.add_intent_handler("unknown_answer", self.answerunknow)
        self.add_intent_handler("tips", self.handle_tips)
        self.add_intent_handler("nidiom", self.nidiom)
        self.add_intent_handler("ai.dueros.common.default_intent", self.handle_default)
        self.add_display_element_selected(self.handle_selected)

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
        mode3 = ListTemplateItem()
        mode1.set_plain_primary_text("闯关模式")
        mode2.set_plain_primary_text("自由模式")
        mode3.set_plain_primary_text("闯关排行榜")
        mode1.set_image(self.commonly_used_image_url_list["entry_mode"])
        mode1.set_image(self.commonly_used_image_url_list["free_mode"])
        mode1.set_image(self.commonly_used_image_url_list["entry_mode_ranking"])
        mode1.set_token("entry_mode")
        mode2.set_token("free_mode")
        mode3.set_token("entry_mode_ranking")
        template.add_item(mode1)
        template.add_item(mode2)
        template.add_item(mode3)

        directive = RenderTemplate(template)
        return {
            "directives": [directive],
            "outputSpeech": r"请选择游戏模式，有不明白的可以像这样问我：小度小度，什么是闯关模式"
        }

    def handle_selected(self, request_data):

        """
        处理请求被选中
        :param request_data: 接收的数据
        :return:
        """
        token = request_data["token"]
        if token == "entry_mode":
            self.handle_entry_mode()
        elif token == "free_mode":
            self.handle_free_mode()
        elif token == "entry_mode_ranking":
            self.handle_entry_mode_ranking()
        else:
            return {
                "outputSpeech": "wrong token! please contact the developer"
            }


    def handle_entry_mode(self):
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

        pos = random.randint(0, len(self.idiom_url_list))

        self.set_session_attribute("pos", pos, None)  # 当前成语id
        self.set_session_attribute("checkpoint_id", 1, 1)  # 第几关
        self.set_session_attribute("round_id", 1, 1)  # 第几轮
        self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
        self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
        self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
        self.set_session_attribute("tips_limit", 8, 8) # 关卡提示次数限制
        self.set_session_attribute("error_limit", 6, 6)  # 关卡错误次数限制
        self.set_session_attribute("round_num", 10, 5) # 本关有多少轮
        self.set_session_attribute("passed_pos", [pos], [])
        self.set_session_attribute("game_mode", "entry_mode", "")

        card = ImageCard()
        card.addItem(self.idiom_url_list[pos][1])
        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"上官——请看题"
        }

    def handle_answer(self):
        
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

        real_pos = int(self.get_session_attribute("pos", None))
        if real_pos is None:
            return {
                "outputSpeech": "we meet an error here, please contact the developer and restart the skill"
            }

        checkpoint_id = int(self.get_session_attribute("checkpoint_id", 1))
        round_id = int(self.get_session_attribute("round_id", 1))
        round_error_num = int(self.get_session_attribute("round_error_num", 0))
        checkpoint_error_num = int(self.get_session_attribute("checkpoint_error_num", 0))
        error_limit = int(self.get_session_attribute("error_limit", 5))
        round_id = int(self.get_session_attribute("round_id", 5))
        passed_pos = list(self.get_session_attribute("passed_pos", []))
        round_num = int(self.get_session_attribute("round_num", 1))
        game_mode = self.get_session_attribute("game_mode", "")
        all_error_num = self.get_session_attribute("all_error_num", 0)

        result = self.get_slots("idiom")
        try:
            user_answer = json.loads(result).get("origin")
        except:
            user_answer = result
        real_answer = self.idiom_url_list[real_pos][0]

        print("user_answer", repr(user_answer))
        print("real_answer", repr(real_answer))

        if not user_answer:
            self.ask("idiom")
            self.wait_answer()
            return {
                "outputSpeech": r"我好像没有理解你的回答，麻烦您再说一遍"
            }
        if user_answer == real_answer:
            # 正确分支
            # ------fix by susnhaolei ----- 因为没有注释，没太看明白代码这几个字段表示的意思，我理解应该是成功之后记录成功次数吗？（emm，这是关卡与轮数的更新）
            if game_mode == "entry_mode":
                if round_id >= round_num:
                    self.set_session_attribute("checkpoint_id", checkpoint_id + 1, 1)  # 关卡加一
                    self.set_session_attribute("round_id", 1, 1)
                    self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
                    self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
                    self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
                    self.set_session_attribute("round_num", 5, 5)  # 本关有多少轮
                    self.set_session_attribute("passed_pos", [], [])
                    new_tips_limit = 8 - checkpoint_id
                    self.set_session_attribute("tips_limit", new_tips_limit, 3)  # 关卡提示次数限制
                    new_error_limit = 4 - checkpoint_id
                    if new_error_limit <= 0:
                        new_error_limit = 1
                    self.set_session_attribute("error_limit", new_error_limit, 5)  # 关卡错误次数限制

                    template = BodyTemplate1()
                    template.set_background_image(self.commonly_used_image_url_list["checkpoint_summary_background"])
                    if checkpoint_error_num == 0:
                        template.set_plain_text_content(
                            r"太棒了！竟然——全部都答对了！对我说'进入下一关'开始第%s关，退出请说'退出'" % (checkpoint_id + 1))
                        directive = RenderTemplate(template)
                        return {
                            "directives": [directive],
                            "outputSpeech": r"太棒了！竟然——全部都答对了！对我说'开始下一关'进入第%s关，退出请说'退出'" % (checkpoint_id + 1)
                        }
                    else:
                        template.set_plain_text_content(
                            r"真棒，你答对了%s题，对我说'进入下一关'开始第" % (round_id - checkpoint_error_num) + "%s关，退出请说：'退出'" % (
                                        checkpoint_id + 1))
                        directive = RenderTemplate(template)
                        return {
                            "directives": [directive],
                            "outputSpeech": r"真棒，你答对了%s题，对我说'进入下一关'开始第" % (
                                        round_num - checkpoint_error_num) + "%s关，退出请说：'退出'" % (checkpoint_id + 1)
                        }

                else:
                    new_pos = random.randint(0, len(self.idiom_url_list))
                    while new_pos in passed_pos:
                        new_pos = random.randint(0, len(self.idiom_url_list))

                    passed_pos.append(new_pos)
                    self.set_session_attribute("round_id", round_id + 1, 1)  # 轮加一
                    self.set_session_attribute("pos", new_pos, None)
                    self.set_session_attribute("round_error_num", 0, 0)
                    self.set_session_attribute("passed_pos", passed_pos, [])

                    card = ImageCard()
                    card.add_item(self.idiom_url_list[new_pos][1])
                    card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                    self.wait_answer()
                    return {
                        "outputSpeech": r"恭喜答对了，您已经闯过了第%s轮，加油！" % round_id,
                        "card": card
                    }
            elif game_mode == "free_mode":
                if len(passed_pos) <= len(self.idiom_url_list):
                    new_pos = random.randint(0, len(self.idiom_url_list))
                    while new_pos in passed_pos:
                        new_pos = random.randint(0, len(self.idiom_url_list))
                else:
                    return {
                        "outputSpeech": "诶呀！这么厉害，一不小心就全部被你猜完啦！我已经没有更多了，谢谢你与我一同玩了这么久，下次再来吧！"
                    }

                passed_pos.append(new_pos)
                self.set_session_attribute("round_id", round_id + 1, 1)  # 轮加一
                self.set_session_attribute("pos", new_pos, None)
                self.set_session_attribute("passed_pos", passed_pos, [])
                self.set_session_attribute("round_error_num", 0, 0)

                card = ImageCard()
                card.add_item(self.idiom_url_list[new_pos][1])
                card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                self.wait_answer()
                return {
                    "outputSpeech": r"恭喜答对了，您已经闯过了%s轮，加油！" % round_id,
                    "card": card
                }
        else:
            # 错误分支
            if game_mode == "entry_mode":
                if checkpoint_error_num+1 > error_limit and round_error_num+1 > 2:
                    self.end_session()
                    return {
                        "outputSpeech": "实在是太遗憾了！你已经在本关里猜错了%s次，请好好磨练自己，改日再来吧！——少年！（我好中二啊哈哈哈）"
                    }
                if round_id >= 10:
                    self.set_session_attribute("checkpoint_id", checkpoint_id + 1, 1)  # 关卡加一
                    self.set_session_attribute("round_id", 1, 1)
                    self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
                    self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
                    self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
                    self.set_session_attribute("round_num", 5, 5)  # 本关有多少轮
                    self.set_session_attribute("passed_pos", [], [])

                    template = BodyTemplate1()
                    template.set_background_image(self.commonly_used_image_url_list["checkpoint_summary_background"])
                    if round_error_num+1 > 2:
                        template.set_plain_text_content(r"这题的答案是%s" % real_answer + "。一共十道题，您答对了%s题。对我说'下一关'即可开始第" % (
                                    round_num - checkpoint_error_num) + "%s轮，退出请说：'退出'" % str(checkpoint_id + 1))
                        directive = RenderTemplate(template)
                        return {
                            "directives": [directive],
                            "outputSpeech": r"这题的答案是%s" % real_answer + "。本关一共%s道题，您答对了%s题。对我说'下一关'即可开始第" % (
                            round_num, (round_num - checkpoint_error_num)) + "%s轮，退出请说：'退出'" % str(checkpoint_id + 1)
                        }

                    else:
                        self.set_session_attribute("round_id", round_id, 1)
                        self.set_session_attribute("pos", real_pos, 0)
                        self.set_session_attribute("round_error_num", round_error_num + 1, 0)
                        self.set_session_attribute("passed_pos", passed_pos, [])
                        card = ImageCard()
                        card.addItem(self.idiom_url_list[real_pos][1])
                        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                        return {
                            "outputSpeech": r"(残念~哒呐)，还是答错了，不要气馁，你还有%s次机会。需要帮助可以说，我需要帮助" % (3 - round_error_num),
                            "card": card
                        }

                else:

                    # self.set_session_attribute("checkpoint_id", checkpoint_id, 0)  # 关卡不变

                    self.wait_answer()
                    if round_error_num+1 > 2:
                        new_pos = random.randint(0, len(self.idiom_url_list))
                        while new_pos in passed_pos:
                            new_pos = random.randint(0, len(self.idiom_url_list))

                        passed_pos.append(new_pos)
                        self.set_session_attribute("round_id", round_id + 1, 0)  # 轮加一
                        self.set_session_attribute("pos", new_pos, 0)
                        self.set_session_attribute("round_error_num", 0, 0)
                        self.set_session_attribute("passed_pos", passed_pos, [])
                        self.set_session_attribute("checkpoint_error_num", checkpoint_error_num + 1, 0)

                        card = ImageCard()
                        card.addItem(self.idiom_url_list[new_pos][1])
                        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                        return {
                            "outputSpeech": "(残念~哒呐)，还是答错了，正确答案是：%s。不过不要气馁，让我们继续吧" % real_answer,
                            "card": card
                        }
                    else:
                        self.set_session_attribute("round_error_num", round_error_num + 1, 0)
                        return {
                            "outputSpeech": r"(残念~哒呐)，还是答错了，不要气馁，你还有%s次机会。需要帮助可以说，我需要帮助" % (3 - round_error_num)
                        }
            elif game_mode == "free_mode":
                if round_error_num+1 > 2:
                    new_pos = random.randint(0, len(self.idiom_url_list))
                    if len(passed_pos) <= len(self.idiom_url_list):
                        while new_pos in passed_pos:
                            new_pos = random.randint(0, len(self.idiom_url_list))
                    else:
                        return {
                            "outputSpeech": "诶呀！这么厉害，一不小心就全部被你猜完啦！我已经没有更多了，谢谢你与我一同玩了这么久，下次再来吧！"
                        }

                    passed_pos.append(new_pos)
                    self.set_session_attribute("round_id", round_id + 1, 0)  # 轮加一
                    self.set_session_attribute("pos", new_pos, 0)
                    self.set_session_attribute("round_error_num", 0, 0)
                    self.set_session_attribute("passed_pos", passed_pos, [])
                    self.set_session_attribute("checkpoint_error_num", checkpoint_error_num + 1, 0)
                    self.set_session_attribute("all_error_num", all_error_num+1, 0)

                    card = ImageCard()
                    card.addItem(self.idiom_url_list[new_pos][1])
                    card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                    return {
                        "outputSpeech": "(残念~哒呐)，还是答错了，正确答案是：%s。不过不要气馁，让我们继续吧" % real_answer,
                        "card": card
                    }
                else:
                    self.set_session_attribute("round_error_num", round_error_num + 1, 0)
                    return {
                        "outputSpeech": r"(残念~哒呐)，还是答错了，不要气馁，你还有%s次机会。需要帮助可以说，我需要帮助，实在不行了也可以说跳过" % (3 - round_error_num)
                    }

    def handle_default(self):

        """
        处理缺省意图
        :return:
        """

        round_error_num = int(self.get_session_attribute("round_error_num", 0))  # 获取错误次数
        self.set_session_attribute("round_error_num", round_error_num+1, 0)  # 增加错误次数

        self.wait_answer()
        return {
            "outputSpeech": r"答错了哦，再努力想想吧，需要帮助可以说，我需要帮助，实在不行了也可以说跳过"
        }

    def handle_now_status(self):

        round_id = str(self.get_session_attribute("round_id", 0))
        checkpoint_id = str(self.get_session_attribute("checkpoint_id", 0))

        self.wait_answer()
        return {
            "outputSpeech": "您现在在第%s关，第%s轮，加油哦！" % (checkpoint_id, round_id)
        }

    def handle_skip(self):

        """
        处理跳过意图
        :return:
        """
        game_mode = self.get_session_attribute("game_mode", "")

        if game_mode == "free_mode":
            passed_pos = self.get_session_attribute("passed_pos", [])
            round_id = self.get_session_attribute("round_id", 1)

            new_pos = random.randint(0, len(self.idiom_url_list))
            if len(passed_pos) <= len(self.idiom_url_list):
                while new_pos in passed_pos:
                    new_pos = random.randint(0, len(self.idiom_url_list))
            else:
                return {
                    "outputSpeech": "诶呀！这么厉害，一不小心就全部被你猜完啦！我已经没有更多了，谢谢你与我一同玩了这么久，下次再来吧！"
                }

            passed_pos.append(new_pos)
            self.set_session_attribute("round_id", round_id+1, 0)  # 轮加一
            self.set_session_attribute("pos", new_pos, 0)
            self.set_session_attribute("round_error_num", 0, 0)
            self.set_session_attribute("passed_pos", passed_pos, [])

            card = ImageCard()
            card.addItem(self.idiom_url_list[new_pos][1])
            card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

            self.wait_answer()
            return {
                "card": card,
                "outputSpeech": "好的，让我们进入第%s轮吧" % round_id+1
            }
        elif game_mode == "enrty_mode":
            return {
                "outputSpeech": "闯关模式是不可以跳过的哦，你个找漏洞的家伙"
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

