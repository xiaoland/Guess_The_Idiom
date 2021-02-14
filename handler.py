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

#   "leavePointInfo": {
#     "game_mode": "",
#     "passed_pos": [],
#     "all_error_num": "",
#     "used_tips_num": "",
#     "checkpoint_id": "",
#     "round_id": "",
#     "error_limit": "",
#     "tips_limit": "",
#     "round_num": "",
#     "can_next_checkpoint": "",
#     "pos": "",
#     "round_error_num": ""
#   }


import random
import json
import os

from dueros.Bot import Bot
from dueros.directive.Display.RenderTemplate import RenderTemplate
from dueros.directive.Display.template.BodyTemplate1 import BodyTemplate1
from dueros.directive.Display.template.ListTemplate1 import ListTemplate1
from dueros.directive.Display.template.ListTemplate4 import ListTemplate4
from dueros.directive.Display.template.ListTemplateItem import ListTemplateItem

from dueros.card.ImageCard import ImageCard
from dueros.card.TextCard import TextCard

from log import Log


class GuessIdiom(Bot):

    def __init__(self, request_data):

        super(GuessIdiom, self).__init__(request_data)
        # fix by sunshaolei 不需要再初始化的时候就随机数，这样每次请求都会重新随机，效率低而且可能随机到重复的(code:random.randint(0:67))

        self.idiom_url_list = json.load(open("./data/json/idiom_url_list.json", "r"))#, encoding="utf-8"))
        self.commonly_used_image_url_list = json.load(
            open("./data/json/commonly_used_image_url_list.json", "r"))#, encoding="utf-8"))
        self.request_data = request_data

        self.log = Log()

        self.log.add_log("Init: New request, initializing...", 1)
        self.log.add_log("Query: %s" % self.get_query(), 1)
        self.wait_answer()

        self.add_launch_handler(self.handle_welcome)
        self.add_session_ended_handler(self.handle_exit)
        self.add_intent_handler("introduce", self.handle_introduce)
        self.add_intent_handler("entry_mode", self.handle_entry_mode)
        self.add_intent_handler("free_mode", self.handle_free_mode)
        self.add_intent_handler("entry_mode_ranking", self.handle_entry_mode_ranking)
        self.add_intent_handler("more", self.handle_more)
        self.add_intent_handler("issue", self.handle_issue)

        self.add_intent_handler("answer_idiom", self.handle_answer)

        self.add_intent_handler("home", self.handle_welcome)
        self.add_intent_handler("skip", self.handle_skip)
        self.add_intent_handler("tips", self.handle_tips)
        self.add_intent_handler("now_status", self.handle_now_status)
        self.add_intent_handler("continue", self.handle_continue)
        self.add_intent_handler("pause", self.handle_pause)
        self.add_intent_handler("next_checkpoint", self.handle_next_checkpoint)

        self.add_intent_handler("ai.dueros.common.cancel_intent", self.handle_welcome)
        self.add_intent_handler("ai.dueros.common.stop_intent", self.handle_pause)
        self.add_intent_handler("ai.dueros.common.default_intent", self.handle_default)

        self.add_display_element_selected(self.handle_selected)

    def handle_introduce(self):

        """
        处理介绍意图
        :return:
        """
        self.log.add_log("handle_introduce: start", 1)
        content = \
        """
        1、闯关模式：设置了关卡，难度递增（不是成语难度，是条件难度），每关错误次数达到一定值就会要求全部重来；
        2、自由模式：没有关卡，想怎么猜怎么猜；
        3、排行榜：目前只支持闯关模式下的排行榜，说“打开排行榜”且为了节省资源，只有在排行榜计算请求>20后才会计算；
        4、每个成语只有3次机会猜，用完了就会视为错误；
        5、说'暂停'来记录信息点，'恢复'来加载信息点；
        6、说'反馈'来上传你遇到的问题或者建议；
        7、本技能由YYH和孙哥哥开发，度秘事业部优化图片，图片来源于网络或二次创作；
        代码地址：https://github.com/xiaoland/Guess_The_Idiom
        说出，返回，来回到模式选择页面
        """
        card = TextCard(content)
        card.set_title("看图猜成语-简介")
        card.add_cue_words(["返回"])
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": content
        }

    def handle_issue(self):

        """
        处理反馈意图
        :return:
        """
        self.log.add_log("handle_issue: start", 1)

        text = self.get_query()
        user_id = self.get_user_id()
        if len(text) == 2:
            output_speech = "请说出你要反馈的内容，像这样，我觉得这里应该这样更好"
        else:
            output_speech = "非常感谢您的反馈，我一定会加油改进的"
            issue_repost = json.load(open("./data/json/issue_report.json", "r", encoding="utf-8"))
            try:
                issue_repost[user_id].append(text)
            except KeyError:
                issue_repost[user_id] = []
                issue_repost[user_id].append(text)

        return {
            "outputSpeech": output_speech
        }

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
        mode4 = ListTemplateItem()
        mode1.set_plain_primary_text("闯关模式")
        mode2.set_plain_primary_text("自由模式")
        mode3.set_plain_primary_text("排行榜")
        mode4.set_plain_primary_text("更多")
        mode1.set_image(self.commonly_used_image_url_list["entry_mode"])
        mode2.set_image(self.commonly_used_image_url_list["free_mode"])
        mode3.set_image(self.commonly_used_image_url_list["entry_mode_ranking"])
        mode4.set_image(self.commonly_used_image_url_list["button_more"])
        mode1.set_token("entry_mode")
        mode2.set_token("free_mode")
        mode3.set_token("entry_mode_ranking")
        mode4.set_token("more")
        template.add_item(mode1)
        template.add_item(mode2)
        template.add_item(mode3)
        template.add_item(mode4)
        self.wait_answer()

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
        self.log.add_log("handle_game_mode_selected: start", 1)
        token = request_data["token"]
        if token == "entry_mode":
            self.log.add_log("entry mode detected", 1)
            return self.handle_entry_mode()
        elif token == "free_mode":
            self.log.add_log("free mode detected", 1)
            return self.handle_free_mode()
        elif token == "entry_mode_ranking":
            self.log.add_log("entry_mode_ranking detected", 1)
            return self.handle_entry_mode_ranking()
        elif token == "more":
            self.log.add_log("more detected", 1)
            return self.handle_more()
        elif token == "issue":
            self.log.add_log("issue detected", 1)
            return self.handle_issue()
        elif token == "introduce":
            self.log.add_log("introduce detected", 1)
            return self.handle_introduce()
        else:
            return {
                "outputSpeech": "wrong token! please contact the developer"
            }

    def handle_entry_mode(self, continue_=False):
        """
        处理闯关模式意图
        :param continue_: 从continue意图触发？
        :return:
        """

        # ------------- fix by sunshaolei -----不要记文件了，记录session吧

        # num = open("./num.txt", "w")
        # wt = self.idiom_url_list[self.number][0] + "000"
        # print(wt)
        # num.write(wt)
        # num.close()

        # ------------- fix by sunshaolei -------
        self.log.add_log("handle_entry_mode: start", 1)

        if continue_ is False:
            pos = random.randint(0, len(self.idiom_url_list))

            self.set_session_attribute("pos", pos, None)  # 当前成语id
            self.set_session_attribute("checkpoint_id", 1, 1)  # 第几关
            self.set_session_attribute("round_id", 1, 1)  # 第几轮
            self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
            self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
            self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
            self.set_session_attribute("tips_limit", 8, 8)  # 关卡提示次数限制
            self.set_session_attribute("error_limit", 6, 6)  # 关卡错误次数限制
            self.set_session_attribute("round_num", 10, 5)  # 本关有多少轮
            self.set_session_attribute("passed_pos", [pos], [])
            self.set_session_attribute("game_mode", "entry_mode", "")
            self.set_session_attribute("can_next_checkpoint", False, False)
            self.set_session_attribute("all_error_num", 0, 0)
        else:
            pos = int(self.get_session_attribute("pos", None))

        user_id = self.get_user_id()
        user_data_list = os.listdir(r"./data/user_data")
        if user_id + ".json" in user_data_list:
            user_data = json.load(open("./data/user_data/%s.json" % user_id, "r", encoding="utf-8"))
        else:
            user_data = json.load(open("./data/json/user_data_template.json", "r", encoding="utf-8"))
            user_data["user_id"] = user_id
            user_data["last_entry_mode_checkpoint_id"] = 1
            json.dump(user_data, open("./data/user_data/%s.json" % user_id, "w", encoding="utf-8"))

        self.set_session_attribute("last_entry_mode_endpoint_id", user_data["lastEntryModeData"]["endpoint_id"], 1)

        card = ImageCard()
        card.add_item(self.idiom_url_list[pos][1])
        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"开始闯关模式。上官——请看题"
        }

    def handle_free_mode(self, continue_=False):

        """
        处理自由模式意图
        :param continue_: 从continue意图触发？
        :return:
        """
        self.log.add_log("handle_free_mode: start", 1)

        if continue_ is False:
            pos = random.randint(0, len(self.idiom_url_list))

            self.set_session_attribute("pos", pos, None)  # 当前成语id
            self.set_session_attribute("checkpoint_id", 1, 1)  # 第几关
            self.set_session_attribute("round_id", 1, 1)  # 第几轮
            self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
            self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
            self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
            self.set_session_attribute("tips_limit", 8, 8)  # 关卡提示次数限制
            self.set_session_attribute("error_limit", 6, 6)  # 关卡错误次数限制
            self.set_session_attribute("round_num", 10, 5)  # 本关有多少轮
            self.set_session_attribute("passed_pos", [pos], [])
            self.set_session_attribute("game_mode", "free_mode", "")
            self.set_session_attribute("can_next_checkpoint", False, False)
            self.set_session_attribute("all_error_num", 0, 0)
        else:
            pos = self.get_session_attribute("pos", None)

        card = ImageCard()
        card.add_item(self.idiom_url_list[pos][1])
        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])
        self.wait_answer()
        return {
            "card": card,
            "outputSpeech": r"开始自由模式。上官——请看题"
        }

    def handle_more(self):

        """
        处理更多
        :return:
        """
        self.log.add_log("handle_more: start", 1)

        self.set_session_attribute("game_mode", "more", "")
        template = ListTemplate1()
        template.set_background_image(self.commonly_used_image_url_list["welcome_background"])
        template.set_token("2")
        template.set_title("看图猜成语-更多")

        info = ListTemplateItem()
        issue = ListTemplateItem()
        info.set_token("introduce")
        issue.set_token("issue")
        info.set_image(self.commonly_used_image_url_list["button_info"])
        issue.set_image(self.commonly_used_image_url_list["button_issue"])
        info.set_plain_primary_text("信息")
        issue.set_plain_primary_text("反馈")
        template.add_item(info)
        template.add_item(issue)
        directive = RenderTemplate(template)

        return {
            "directives": [directive]
        }

    def handle_entry_mode_ranking(self):

        """
        处理闯关模式排行榜意图
        :return:
        """
        self.log.add_log("handle_entry_mode_ranking: start", 1)

        user_id = self.get_user_id()
        user_data_list = os.listdir(r"./data/user_data")
        if user_id + ".json" in user_data_list:
            user_data = json.load(open("./data/user_data/%s.json" % user_id, "r", encoding="utf-8"))
        else:
            user_data = json.load(open("./data/json/user_data_template.json", "r", encoding="utf-8"))
            user_data["user_id"] = user_id
            json.dump(user_data, open("./data/user_data/%s.json" % user_id, "w", encoding="utf-8"))
            self.compute_ranking()

        user_ranking = user_data["ranking"]

        template = ListTemplate4()
        # template.set_background_image(self.commonly_used_image_url_list["entry_mode_ranking_background"])
        template.set_title("闯关模式排行榜")
        template.set_plain_text_content("你：第%s名" % user_ranking)

        ranking_data = json.load(open("./data/json/ranking.json", "r", encoding="utf-8"))
        for index in range(1, 16):
            item = ListTemplateItem()
            try:
                item.set_plain_primary_text("第%s名：" % (index) + ranking_data[index-1])
            except KeyError:
                self.compute_ranking()
                return {
                    "outputSpeech": "请等待排行榜进行计算"
                }
            template.add_item(item)
            
        

        directive = RenderTemplate(template)
        return {
            "directives": [directive],
            "outputSpeech": r"喏，你要的排名"
        }

    def handle_answer(self, user_answer=None):

        """
        处理回答成语意图
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
        self.log.add_log("answer_idiom: start handle", 1)

        try:
            real_pos = int(self.get_session_attribute("pos", None))
        except TypeError:
            self.log.add_log("handle_answer: get pos fail with None", 3)
            return {
                "我不是很明白，可以麻烦你再说一遍吗"
            }
        if real_pos is None:
            return {
                "outputSpeech": "we meet an error here, please contact the developer and restart the skill"
            }

        checkpoint_id = int(self.get_session_attribute("checkpoint_id", 1))
        round_id = int(self.get_session_attribute("round_id", 1))
        round_error_num = int(self.get_session_attribute("round_error_num", 0))
        checkpoint_error_num = int(self.get_session_attribute("checkpoint_error_num", 0))
        error_limit = int(self.get_session_attribute("error_limit", 5))
        # round_id = int(self.get_session_attribute("round_id", 5))
        passed_pos = list(self.get_session_attribute("passed_pos", []))
        round_num = int(self.get_session_attribute("round_num", 1))
        game_mode = self.get_session_attribute("game_mode", "")
        all_error_num = self.get_session_attribute("all_error_num", 0)

        if user_answer is None:
            result = self.get_slots("idiom")
            try:
                user_answer = json.loads(result).get("origin")
            except:
                user_answer = result
        real_answer = self.idiom_url_list[real_pos][0]

        print("user_answer", user_answer)
        print("real_answer", real_answer)

        if not user_answer:
            self.log.add_log("answer is none, ask", 1)
            self.ask("idiom")
            self.wait_answer()
            return {
                "outputSpeech": r"我好像没有理解你的回答，麻烦您再说一遍"
            }
        if real_answer in user_answer or user_answer == real_answer:
            # 正确分支
            # ------fix by susnhaolei ----- 因为没有注释，没太看明白代码这几个字段表示的意思，我理解应该是成功之后记录成功次数吗？（emm，这是关卡与轮数的更新）
            self.log.add_log("answer is correct", 1)
            if game_mode == "entry_mode":
                if round_id >= round_num:
                    self.log.add_log("next checkpoint is allowed now", 1)

                    self.set_session_attribute("checkpoint_id", checkpoint_id + 1, 1)  # 关卡加一
                    self.set_session_attribute("round_id", 1, 1)
                    self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
                    self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
                    self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
                    self.set_session_attribute("round_num", 5, 5)  # 本关有多少轮
                    self.set_session_attribute("passed_pos", [], [])
                    self.set_session_attribute("can_next_checkpoint", True, False)
                    new_tips_limit = 8 - checkpoint_id
                    self.set_session_attribute("tips_limit", new_tips_limit, 3)  # 关卡提示次数限制
                    new_error_limit = 4 - checkpoint_id
                    if new_error_limit <= 0:
                        new_error_limit = 1
                    self.set_session_attribute("error_limit", new_error_limit, 5)  # 关卡错误次数限制

                    template = BodyTemplate1()
                    template.set_background_image(self.commonly_used_image_url_list["checkpoint_summary_background"])

                    if checkpoint_error_num == 0:
                        self.log.add_log("all correct in one checkpoint", 1)
                        template.set_plain_text_content(
                            r"太棒了！竟然——全部都答对了！对我说'进入下一关'开始第%s关，退出请说'退出'，对我说反馈即可立马反馈" % (checkpoint_id + 1))
                        directive = RenderTemplate(template)
                        return {
                            "directives": [directive],
                            "outputSpeech": r"太棒了！竟然——全部都答对了！对我说'开始下一关'进入第%s关，退出请说'退出'，对我说反馈即可立马反馈" % (checkpoint_id + 1)
                        }
                    else:
                        self.log.add_log("partially correct in one checkpoint", 1)
                        template.set_plain_text_content(
                            r"真棒，你答对了%s题，对我说'进入下一关'开始第" % (round_id - checkpoint_error_num) + "%s关，退出请说：'退出'" % (
                                    checkpoint_id + 1))
                        directive = RenderTemplate(template)
                        return {
                            "directives": [directive],
                            "outputSpeech": r"真棒，你答对了%s题，对我说'进入下一关'开始第" % (
                                    round_num - checkpoint_error_num) + "%s关，退出请说：'退出'，对我说反馈即可立马反馈" % (checkpoint_id + 1)
                        }

                else:
                    self.log.add_log("next round will be execute", 1)

                    if len(passed_pos) < len(self.idiom_url_list):
                        new_pos = random.randint(0, len(self.idiom_url_list))
                        while new_pos in passed_pos:
                            new_pos = random.randint(0, len(self.idiom_url_list))
                    else:
                        template = ImageCard() # BodyTemplate1()
                        template.add_item(self.commonly_used_image_url_list["entry_mode_pass"])
                        # template.set_plain_text_content("恭喜魔鬼，你成功通关了「闯关模式」")
                        # directive = RenderTemplate(template)
                        self.compute_ranking()
                        return {
                            # "directives": [directive],
                            "card": template,
                            "outputSpeech": "我的上帝，你是什么魔鬼，闯关模式都被你攻略了！可以去隔壁了"
                        }

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
                    self.log.add_log("no more pos can be selected", 1)
                    self.handle_exit()
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
            self.log.add_log("answer is fault", 1)
            if game_mode == "entry_mode":
                if checkpoint_error_num + 1 > error_limit and round_error_num + 1 > 2:
                    self.log.add_log("exit entry mode because checkpoint_error_num is limit reached", 1)
                    self.clear_user_lp_info()
                    self.handle_exit()
                    return {
                        "outputSpeech": "实在是太遗憾了！你已经在本关里猜错了%s次，请好好磨练自己，改日再来吧！——少年！（我好中二啊哈哈哈）"
                    }
                if round_id >= 10:
                    self.log.add_log("next checkpoint is allowed now", 1)

                    self.set_session_attribute("round_id", 1, 1)
                    self.set_session_attribute("checkpoint_error_num", 0, 0)  # 本关错误次数
                    self.set_session_attribute("round_error_num", 0, 0)  # 本轮错误次数
                    self.set_session_attribute("used_tips_num", 0, 0)  # 本关使用的提示数
                    self.set_session_attribute("round_num", 5, 5)  # 本关有多少轮
                    self.set_session_attribute("passed_pos", [], [])
                    self.set_session_attribute("can_next_checkpoint", True, False)

                    template = BodyTemplate1()
                    template.set_background_image(self.commonly_used_image_url_list["checkpoint_summary_background"])
                    if round_error_num + 1 > 2:
                        self.set_session_attribute("checkpoint_id", checkpoint_id + 1, 1)  # 关卡加一
                        self.log.add_log("next round is allow now because round_error_num limit reached", 1)
                        template.set_plain_text_content(r"这题的答案是%s" % real_answer + "。一共十道题，您答对了%s题。对我说'下一关'即可开始第" % (
                                round_num - checkpoint_error_num) + "%s轮，退出请说：'退出'" % str(checkpoint_id + 1))
                        directive = RenderTemplate(template)
                        return {
                            "directives": [directive],
                            "outputSpeech": r"这题的答案是%s" % real_answer + "。本关一共%s道题，您答对了%s题。对我说'下一关'即可开始第" % (
                                round_num, (round_num - checkpoint_error_num)) + "%s轮，退出请说：'退出'" % str(
                                checkpoint_id + 1)
                        }

                    else:
                        self.set_session_attribute("round_id", round_id, 1)
                        self.set_session_attribute("pos", real_pos, 0)
                        self.set_session_attribute("round_error_num", round_error_num + 1, 0)
                        self.set_session_attribute("passed_pos", passed_pos, [])
                        card = ImageCard()
                        card.add_item(self.idiom_url_list[real_pos][1])
                        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                        return {
                            "outputSpeech": r"(残念~哒呐)，还是答错了，不要气馁，你还有%s次机会。需要帮助可以说，我需要帮助" % (2 - round_error_num),
                            "card": card
                        }

                else:

                    # self.set_session_attribute("checkpoint_id", checkpoint_id, 0)  # 关卡不变

                    self.wait_answer()
                    if round_error_num + 1 > 2:
                        self.log.add_log("next round is allow now because round_error_num limit reached", 1)

                        if len(passed_pos) < len(self.idiom_url_list):
                            new_pos = random.randint(0, len(self.idiom_url_list))
                            while new_pos in passed_pos:
                                new_pos = random.randint(0, len(self.idiom_url_list))
                        else:
                            template = BodyTemplate1()
                            template.set_background_image(self.commonly_used_image_url_list["entry_mode_pass"])
                            template.set_plain_text_content("虽然你这题错了，我也很不情愿，但不得不恭喜你成功通关了「闯关模式」")
                            directive = RenderTemplate(template)
                            self.compute_ranking()
                            return {
                                "directives": [directive],
                                "outputSpeech": "虽然你这题错了，我也很不情愿，但不得不恭喜你这位魔鬼成功通关了「闯关模式」"
                            }

                        passed_pos.append(new_pos)
                        self.set_session_attribute("round_id", round_id + 1, 0)  # 轮加一
                        self.set_session_attribute("pos", new_pos, 0)
                        self.set_session_attribute("round_error_num", 0, 0)
                        self.set_session_attribute("passed_pos", passed_pos, [])
                        self.set_session_attribute("checkpoint_error_num", checkpoint_error_num + 1, 0)

                        card = ImageCard()
                        card.add_item(self.idiom_url_list[new_pos][1])
                        card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                        return {
                            "outputSpeech": "(残念~)，还是答错了，正确答案是：%s。不过不要气馁，让我们继续吧" % real_answer,
                            "card": card
                        }
                    else:
                        self.set_session_attribute("round_error_num", round_error_num + 1, 0)
                        return {
                            "outputSpeech": r"(残念~)，还是答错了，不要气馁，你还有%s次机会。需要帮助可以说，我需要帮助" % (2 - round_error_num)
                        }
            elif game_mode == "free_mode":
                if round_error_num + 1 > 2:
                    new_pos = random.randint(0, len(self.idiom_url_list))
                    if len(passed_pos) <= len(self.idiom_url_list):
                        while new_pos in passed_pos:
                            new_pos = random.randint(0, len(self.idiom_url_list))
                    else:
                        self.log.add_log("no more pos can be selected", 1)
                        self.handle_exit()
                        return {
                            "outputSpeech": "诶呀！这么厉害，一不小心就全部被你猜完啦！我已经没有更多了，谢谢你与我一同玩了这么久，下次再来吧！"
                        }

                    passed_pos.append(new_pos)
                    self.set_session_attribute("round_id", round_id + 1, 0)  # 轮加一
                    self.set_session_attribute("pos", new_pos, 0)
                    self.set_session_attribute("round_error_num", 0, 0)
                    self.set_session_attribute("passed_pos", passed_pos, [])
                    self.set_session_attribute("checkpoint_error_num", checkpoint_error_num + 1, 0)
                    self.set_session_attribute("all_error_num", all_error_num + 1, 0)

                    card = ImageCard()
                    card.add_item(self.idiom_url_list[new_pos][1])
                    card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

                    return {
                        "outputSpeech": "(残念~哒呐)，还是答错了，正确答案是：%s。不过不要气馁，让我们继续吧" % real_answer,
                        "card": card
                    }
                else:
                    self.set_session_attribute("round_error_num", round_error_num + 1, 0)
                    return {
                        "outputSpeech": r"(残念~哒呐)，还是答错了，不要气馁，你还有%s次机会。需要帮助可以说，我需要帮助，实在不行了也可以说跳过" % (2 - round_error_num)
                    }

    def handle_default(self):

        """
        处理缺省意图
        :return:
        """
        self.log.add_log("handle_default: start", 1)
        game_mode = self.get_session_attribute("game_mode", "")

        self.wait_answer()

        if game_mode != "" or game_mode != "more":
            text = self.get_query()

            if len(text) == 4:
                return self.handle_answer()
            elif 0<= len(text) < 4:
                output_speech = "不好意思，我不是很明白，可以麻烦再说一遍吗"
            else:
                round_error_num = int(self.get_session_attribute("round_error_num", 0))  # 获取错误次数
                self.set_session_attribute("round_error_num", round_error_num + 1, 0)  # 增加错误次数
                output_speech = "答错了哦，再努力想想吧，需要帮助可以说，我需要帮助，实在不行了也可以说跳过，需要暂停可以说暂停，之后恢复即可"
        else:
            output_speech = "不好意思，我不是很明白，可以麻烦再说一遍吗"

        return {
            "outputSpeech": output_speech
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

        self.wait_answer()
        if game_mode == "free_mode":
            passed_pos = self.get_session_attribute("passed_pos", [])
            round_id = self.get_session_attribute("round_id", 1)

            new_pos = random.randint(0, len(self.idiom_url_list))
            if len(passed_pos) <= len(self.idiom_url_list):
                while new_pos in passed_pos:
                    new_pos = random.randint(0, len(self.idiom_url_list))
            else:
                self.handle_exit()
                self.log.add_log("no more pos can be selected", 1)
                return {
                    "outputSpeech": "诶呀！这么厉害，一不小心就全部被你猜完啦！我已经没有更多了，谢谢你与我一同玩了这么久，下次再来吧！"
                }

            passed_pos.append(new_pos)
            self.set_session_attribute("round_id", round_id + 1, 0)  # 轮加一
            self.set_session_attribute("pos", new_pos, 0)
            self.set_session_attribute("round_error_num", 0, 0)
            self.set_session_attribute("passed_pos", passed_pos, [])

            card = ImageCard()
            card.add_item(self.idiom_url_list[new_pos][1])
            card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

            self.wait_answer()
            return {
                "card": card,
                "outputSpeech": "好的，让我们进入第%s轮吧" % round_id + 1
            }
        elif game_mode == "enrty_mode":
            return {
                "outputSpeech": "闯关模式是不可以跳过的哦，你个找漏洞的家伙"
            }

    def handle_pause(self):

        """
        处理暂停意图：存储离开点
        :return:
        """
        self.log.add_log("handle_pause: start", 1)
        user_id = self.get_user_id()

        game_mode = self.get_session_attribute("game_mode", "")
        self.log.add_log("game_mode: %s" % game_mode, 1)
        if game_mode != "" or game_mode != "more":
            self.wait_answer()
            leave_point_info = {
                "game_mode": game_mode,
                "passed_pos": self.get_session_attribute("passed_pos", []),
                "all_error_num": self.get_session_attribute("all_error_num", 0),
                "used_tips_num": self.get_session_attribute("used_tips_num", 0),
                "checkpoint_id": self.get_session_attribute("checkpoint_id", 1),
                "round_id": self.get_session_attribute("round_id", 1),
                "error_limit": self.get_session_attribute("error_limit", 1),
                "tips_limit": self.get_session_attribute("tips_limit", 1),
                "round_num": self.get_session_attribute("round_num", 1),
                "can_next_checkpoint": self.get_session_attribute("can_next_checkpoint", False),
                "pos": self.get_session_attribute("pos", 0),
                "round_error_num": self.get_session_attribute("round_error_num", 0),
                "checkpoint_error_num": self.get_session_attribute("checkpoint_error_num", 0)
            }
            user_data_list = os.listdir(r"./data/user_data")
            if user_id + ".json" in user_data_list:
                user_data = json.load(open("./data/user_data/%s.json" % user_id, "r", encoding="utf-8"))
            else:
                user_data = json.load(open("./data/json/user_data_template.json", "r", encoding="utf-8"))
                user_data["user_id"] = user_id

            user_data["leavePointInfo"] = leave_point_info
            json.dump(user_data, open("./data/user_data/%s.json" % user_id, "w", encoding="utf-8"))
            return {
                "outputSpeech": "暂停完成！信息点已经记录"
            }
        else:
            return {
                "outputSpeech": "请先开始游戏，这样我才能记录你的游戏信息"
            }

    def handle_continue(self):

        """
        处理继续意图: 从离开的地方继续
        :return:
        """
        self.log.add_log("handle_continue: start", 1)

        self.wait_answer()
        output_speech = ""
        user_id = self.get_user_id()
        user_data_list = os.listdir(r"./data/user_data")
        if user_id + ".json" in user_data_list:
            self.log.add_log("user_id-%s is exist" % user_id, 1)
            user_data = json.load(open("./data/user_data/%s.json" % user_id, "r", encoding="utf-8"))
            if user_data["leavePointInfo"] is None:
                self.log.add_log("user_id-%s does not pause ever to record LP info" % user_id, 2)
                output_speech = "你还没有暂停过来存储信息呢！"
            else:
                lp_info = user_data["leavePointInfo"]
                self.set_session_attribute("pos", lp_info["pos"], None)  # 当前成语id
                self.set_session_attribute("checkpoint_id", lp_info["checkpoint_id"], 1)  # 第几关
                self.set_session_attribute("round_id", lp_info["round_id"], 1)  # 第几轮
                self.set_session_attribute("checkpoint_error_num", lp_info["checkpoint_error_num"], 0)  # 本关错误次数
                self.set_session_attribute("round_error_num", lp_info["round_error_num"], 0)  # 本轮错误次数
                self.set_session_attribute("used_tips_num", lp_info["used_tips_num"], 0)  # 本关使用的提示数
                self.set_session_attribute("tips_limit", lp_info["tips_limit"], 8)  # 关卡提示次数限制
                self.set_session_attribute("error_limit", lp_info["error_limit"], 6)  # 关卡错误次数限制
                self.set_session_attribute("round_num", lp_info["round_num"], 5)  # 本关有多少轮
                self.set_session_attribute("passed_pos", lp_info["passed_pos"], [])
                self.set_session_attribute("game_mode", lp_info["game_mode"], "")
                self.set_session_attribute("can_next_checkpoint", lp_info["can_next_checkpoint"], False)
                self.set_session_attribute("all_error_num", lp_info["all_error_num"], 0)

                game_mode = lp_info["game_mode"]
                if game_mode == "entry_mode":
                    return self.handle_entry_mode(continue_=True)
                elif game_mode == "free_mode":
                    return self.handle_free_mode(continue_=True)
                elif game_mode == "entry_mode_ranking":
                    return self.handle_entry_mode_ranking()
                elif game_mode == "more":
                    return self.handle_more()
        else:
            self.log.add_log("user_id-%s is not exist" % user_id, 1)
            output_speech = "你还没有暂停过来存储信息呢！"

        return {
            "outputSpeech": output_speech
        }

    def handle_tips(self):

        """
        处理提示
        :return:
        """
        self.log.add_log("handle_tips: start", 1)
        output_speech = ""
        self.wait_answer()

        game_mode = self.get_session_attribute("game_mode", "")
        pos = int(self.get_session_attribute("pos", 0))
        used_tips_num = self.get_session_attribute("used_tips_num", 0)

        real_answer = self.idiom_url_list[pos][0]

        if game_mode == "free_mode":
            number = random.randint(2, 4)
            self.set_session_attribute("used_tips_num", used_tips_num + 1, 0)
            if number == 2:
                # card = TextCard("上官，答案的第一个字是%s" % real_answer[0])
                output_speech = "上官，答案的第一个字是%s" % real_answer[0]
            elif number == 3:
                # card = TextCard("皇上，答案的前两个字是%s" % (real_answer[0] + real_answer[1]))
                output_speech = "皇上，答案的前两个字是%s" % (real_answer[0] + real_answer[1])
            elif number == 4:
                # card = TextCard("诶呀，成语躲起来了，加油想一想吧")
                output_speech = "诶呀！成语躲起来了，加油想一想吧"

        elif game_mode == "entry_mode":
            tips_limit = self.get_session_attribute("tips_limit", 0)

            if used_tips_num <= tips_limit:
                number = random.randint(2, 3)
                remain_tips_num = tips_limit - (used_tips_num + 1)
                self.set_session_attribute("used_tips_num", used_tips_num + 1, 0)

                if number == 2:
                    output_speech = "上官，答案的第一个字是%s" % real_answer[0] + "。你还剩%s次提示机会" % remain_tips_num
                elif number == 3:
                    output_speech = "皇上，答案的前两个字是%s" % (
                                real_answer[0] + real_answer[1]) + "。你还剩%s次提示机会" % remain_tips_num

            else:
                output_speech = "本关的提示使用次数已经用完了，送你一个'危'字"

        return {
            "outputSpeech": output_speech
        }

    def handle_next_checkpoint(self):

        """
        处理下一关意图
        :return:
        """
        self.log.add_log("handle_next_checkpoint: start", 1)
        can_next_checkpoint = self.get_session_attribute("can_next_checkpoint", False)

        if can_next_checkpoint:
            self.set_session_attribute("can_next_checkpoint", False, False)
            self.compute_ranking()

            checkpoint_id = self.get_session_attribute("checkpoint_id", 1)
            passed_pos = self.get_session_attribute("passed_pos", [])

            if len(passed_pos) < len(self.idiom_url_list):
                new_pos = random.randint(0, len(self.idiom_url_list))
                while new_pos in passed_pos:
                    new_pos = random.randint(0, len(self.idiom_url_list))
            else:
                template = BodyTemplate1()
                template.set_background_image(self.commonly_used_image_url_list["entry_mode_pass"])
                template.set_plain_text_content("恭喜魔鬼，你成功通关了「闯关模式」")
                directive = RenderTemplate(template)
                self.compute_ranking()
                return {
                    "directives": [directive],
                    "outputSpeech": "我的上帝，你是什么魔鬼，闯关模式都被你攻略了！可以去隔壁了"
                }

            passed_pos.append(new_pos)
            self.set_session_attribute("pos", new_pos, None)
            self.set_session_attribute("passed_pos", passed_pos, [])

            card = ImageCard()
            card.add_item(self.idiom_url_list[new_pos][1])
            card.add_cue_words(["我觉得答案是...", "（你的成语答案）", "我需要帮助/我不知道答案"])

            self.wait_answer()
            return {
                "card": card,
                "outputSpeech": "好的，让我们进入第%s关"%checkpoint_id
            }
        else:
            return {
                "outputSpeech": "Sir!你还不可以进入下一关呢！"
            }

    def handle_exit(self):

        """
        处理退出意图
        :return:
        """
        self.log.add_log("handle_exit: start", 1)
        game_mode = self.get_session_attribute("game_mode", "")
        if game_mode == "entry_mode":
            self.record_user_info()
            self.compute_ranking()
        self.end_session()
        return {
            "outputSpeech": "好的呢，小的告退——，即便如此，您仍可以说，继续游戏来加载上次记录的信息点"
        }

    def clear_user_lp_info(self):

        """
        清空用户记录点
        :return:
        """
        self.log.add_log("clear_user_lp_info: start", 1)
        user_id = self.get_user_id()
        self.log.add_log("clear user_id-%s's lp info" % user_id, 1)

        user_data_list = os.listdir("./data/user_data")
        if user_id + ".json" in user_data_list:
            user_data = json.load(open("./data/user_data/%s.json" % user_id, "r", encoding="utf-8"))
            user_data["leavePointInfo"] = None
            json.dump(user_data, open("./data/user_data/%s.json" % user_id, "w", encoding="utf-8"))

    def record_user_info(self):

        """
        记录用户信息
        :return:
        """
        self.log.add_log("record_user_info: start", 1)

        user_id = self.get_user_id()

        user_data_list = os.listdir("./data/user_data")
        if user_id + ".json" in user_data_list:
            user_data = json.load(open("./data/user_data/%s.json" % user_id, "r", encoding="utf-8"))
        else:
            user_data = json.load(open("./data/json/user_data_template.json", "r", encoding="utf-8"))

        user_data["lastEntryModeData"]["endpoint_id"] = int(str(self.get_session_attribute("checkpoint_id")) + str(self.get_session_attribute("round_id")))
        user_data["lastEntryModeData"]["used_tips_num"] = int(self.get_session_attribute("used_tips_num"))
        user_data["lastEntryModeData"]["checkpoint_error_num"] = int(self.get_session_attribute("checkpoint_error_num"))

        json.dump(user_data, open("./data/user_data/%s.json" % user_id, "w", encoding="utf-8"))

    def compute_ranking(self):

        """
        计算排名
        :return:
        """
        self.log.add_log("compute_ranking: start", 1)

        compute_request_count = int(open("./data/compute_ranking_request.txt", "r").read())
        if compute_request_count >= 20:
            self.log.add_log("compute_ranking: over 20 request time, start compute", 1)
            open("./data/compute_ranking_request.txt", "w").write("0")

            # raw_data = []
            base_ranking_data = {}
            user_id_list = os.listdir("./data/user_data")
            for user_id_file in user_id_list:
                user_data = json.load(open("./data/user_data/%s" % user_id_file, "r", encoding="utf-8"))
                # raw_data.append([user_data["user_id"], user_data["lastEntryModeData"]])
                base_ranking_data[int(user_data["lastEntryModeData"]["endpoint_id"])] = user_data["user_id"]

            base_ranking_list = json.load(open("./data/json/ranking.json", "r", encoding="utf-8"))
            base_ranking_data_index = list(base_ranking_data.keys())
            base_ranking_data_index.sort(reverse=True)
            for index in base_ranking_data_index:
                base_ranking_list[index] = base_ranking_data[index]
                
            json.dump(base_ranking_list, open("./data/json/ranking.json", "w", encoding="utf-8"))

            # for user_data in raw_data:
        else:
            self.log.add_log("compute_ranking: less than 20, add one", 1)
            open("./data/compute_ranking_request.txt", "w").write(str(compute_request_count+1))


if __name__ == "__main__":
    pass
