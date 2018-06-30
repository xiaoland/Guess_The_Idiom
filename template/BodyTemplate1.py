#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# author:sunshaolei

from dueros.directive.BaseDirective import BaseDirective

class BodyTemplate1(BaseDirective):
    """
    卡片形式展示
    """

    def __init__(self):
        '''
        文本卡片显示的content
        :param content:
        '''
        super(BodyTemplate1, self).__init__('BodyTemplate1')


    def setBackGroundImage(self, url, widthPixels=0, heightPixels=0):
        self.data["setBackgroundImage"] = {
            "url": url,
            "widthPixels": widthPixels,
            "heightPixels": heightPixels,
        }

    def setTitle(self, title):
        self.data["title"] = title

    def setTextContent(self, text):
        self.data["content"] = {
            "type": "PlainText",
            "text": text
        }



