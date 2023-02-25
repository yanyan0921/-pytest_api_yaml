#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/14 
@Author  : LL
@File    : parameter_setting.py
参数处理
'''
from jsonpath import jsonpath

from tool import request_data_nest_replace
from tool.log import logger
from tool.function import random_str, random_time, random_number


class ParameterSetting:
    access_value = {}

    @classmethod
    def data_is_replace(cls, data):
        '''
        :param data: 请求参数data和提取参数extract_key
        :return: 返回参数是否需要被替换
        '''
        if data is None:
            return False
            # 请求参数是单纯一个列表格式的情况
        if type(data) == list:
            for i in data:
                if '$.' in str(i) or 'random' in str(i):
                    return 'list_request'
            return False
            # 先检查是否有嵌套参数里面有指定替换格式,然后$.然后random
        for k, v in data.items():
            if '^' in str(v) or '$.' in str(v) or 'random' in str(v):
                return True
        return False

    @classmethod
    def parameter_setting_list(cls, data: list):
        i_wz = 0
        for i in data:
            if '$.' in str(i):
                data[i_wz] = jsonpath(cls.access_value, i)[0]
            if 'random' in str(i):
                data[i_wz] = eval(i)
            i_wz += 1
        return data
    @classmethod
    def parameter_setting_dict(cls, data: dict, type='get'):
        '''
        :param data: 返回结果提取和参数依赖使用dict 例：{'bill': '$.bill'}
        :param type: save ：把数据存到参数池里面无返回，get读取参数池数据并返回新值
        :return:
        '''

        if type == 'save':
            for k, v in data.items():
                cls.access_value[k] = v
            logger.info(f'参数提取完成后的参数池：{cls.access_value}')
            print(1)
        if type == 'get':
            for k, v in data.items():
                '''请求多级嵌套'''
                if '^' in str(v):
                    v = request_data_nest_replace(cls.access_value, v)
                data[k] = v
                '''请求参数只有一个层级'''
                if '$.' in str(v):
                    if not jsonpath(cls.access_value, v):
                        logger.error(f'依赖参数出现问题，依赖表达式{v}，参数池{cls.access_value}')
                        return {'错误信息': '未读取到参数'}
                    logger.info(f'读取前的参数池{cls.access_value}')
                    v = jsonpath(cls.access_value, v)[0]
                    data[k] = v
            for k, v in data.items():
                if 'random' in str(v):
                    data[k] = eval(v)
            return data

    @classmethod
    def extract_value(cls, api_response: dict, extract_key: dict):
        '''
        :param extract_key: {'billCommonNo': '$.content.billCommonNo'} 提取参数字典
        :return: 返回通过表达式提取出接口的最终要存的值
        '''
        extract_value = {}
        for k, v in extract_key.items():
            extract_value[k] = jsonpath(api_response, v)[0]
        return extract_value


if __name__ == '__main__':
    ParameterSetting.parameter_setting_dict({'a': 44, 'a1': 144, 'b': 1, 'g': 'wbg'}, 'save')

    ParameterSetting.parameter_setting_dict({'b': '$.b', 'g': '$.g'})
    print(f'最终的参数池{ParameterSetting.access_value}')

    # print(ParameterSetting.extract_value({'data':{'id':'1'}},{'id':'$.data.id'}))
