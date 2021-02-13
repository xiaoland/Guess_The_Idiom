#!/usr/bin/env python3
# -*- encoding=utf-8 -*-

# description:
# author:jack
# create_time: 2018/1/5

"""
    desc:pass
"""
import json
import time


class Utils(object):

    @staticmethod
    def checkKeyInDict(dicts, key):
        '''
        校验字典中是否存在指定的key
        :param dicts:
        :param key:
        :return:
        '''
        if(isinstance(dicts, dict)):
            return key in dicts
        return False

    @staticmethod
    def checkKeysInDict(dicts, keys):

        if isinstance(dicts, str):
            dicts = json.loads(dicts)
        lastKey = keys[len(keys)-1]
        for key in keys:
            if key in dicts:
                dicts = dicts[key]
                if lastKey == key:
                    return True
                continue
            return False

    @staticmethod
    def getDictDataByKeys(dicts, keys):
        if isinstance(dicts, dict):
            for key in keys:
                if key in dicts:
                    v = dicts[key]
                    if isinstance(v, dict):
                        dicts = v
                        continue
                    elif isinstance(v, str):
                        return v


    @staticmethod
    def get_dict_data_by_keys(dicts, keys):
        if isinstance(dicts, str):
            dicts = json.loads(dicts)
        last_key = keys[len(keys) - 1]
        for key in keys:
            if key in dicts:
                dicts = dicts[key]
                if dicts is None:
                    return None
                if last_key == key:
                    return dicts
                continue
            return None


    @staticmethod
    def is_numeric(value):
        if isinstance(value, str):
            return type(eval(value)) == int or type(eval(value)) == float
        else:
            return isinstance(value, int) or isinstance(value, float)

    @staticmethod
    def convert_number(value):
        if Utils.is_numeric(value):

            if isinstance(value, str):
                if type(eval(value)) == int:
                    return int(value)
                if type(eval(value)) == float:
                    return int(float(value))

            if isinstance(value, int) or isinstance(value, float):
                return int(value)

    @staticmethod
    def get_millisecond():
        '''
        获取当前时间
        :return:
        '''

        return int(time.time())


if __name__ == '__main__':
    pass