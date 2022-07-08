#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

import requests
from jsonpath import jsonpath

from config.config import Environment
from tool.read_file import ReadFile


def get_ip():
    '''获取本机ip地址'''
    import socket
    res = socket.gethostbyname(socket.gethostname())
    return res


def int_replace_str(new_dict_v):
    '''
    把列表或者字典多层嵌套里面的带有int标识的字符转为数字类型
    :param new_dict_v: 多层请求参数嵌套被jsonpath替换后的新值,有int标识就处理，没有就当没运行这方法
    :return: 把'int292174' 这种变为  292174
    '''
    if isinstance(new_dict_v, list):
        for i in new_dict_v:
            if isinstance(i, dict):
                for k, v in i.items():
                    if v != None and type(v) != bool:
                        if 'int' in v:
                            new_v = v[3:len(v) + 1]
                            i[k] = int(new_v)
        print(f'new_dict_v={new_dict_v}')
        return new_dict_v
    elif isinstance(new_dict_v, dict):
        print('最外层现在只支持列表,里面嵌套多个字典')
    else:
        print('最外层现在只支持列表,里面嵌套多个字典')


def request_data_nest_replace(access_value, dict_v):
    '''
    请求参数多层嵌套，处理嵌套里面的jsonpath表达式转为值，
    但是数字也会被变为字符串，加标识再写一个方法（int_replace_str）进行处理
    :access_value :参数池
    :param dict_v: 多层嵌套参数的值当前支持的格式[{},{}]
    :return: 多层请求参数被替换后的值
    '''
    replace_list = re.findall('\^(.*?)\^', str(dict_v))
    for i in replace_list:
        replace_value = jsonpath(access_value, i)
        if replace_value != False:
            bei_replace = f'^{i}^'  # '^$.waybillid^'
            replace_value = replace_value[0]
            if type(replace_value) == int:
                dict_v = str(dict_v).replace(bei_replace, 'int' + str(replace_value))
            else:
                dict_v = str(dict_v).replace(bei_replace, str(replace_value))
    new_dict_v = int_replace_str(eval(dict_v))
    return new_dict_v


def requests_environment_info(environment=Environment):
    '''
    :return: 返回ip和headers信息
    '''
    # 配置文件信息
    try:
        env_info = ReadFile.read_yaml('config/environment.yaml')
        # 测试环境配置文件相关信息
        request_info = env_info[Environment]
        return {'ip': request_info['http'] + request_info['domain_name'], 'headers': request_info['headers']}
    except Exception as e:
        print(f'读取配置信息出错：{e}')


def get_token():
    # 这个不要在意细节，我这个接口比较自己弄的，反正这里写怎么获得token就行
    headers = {'token': 'em123dca666333'}
    token = requests.get(f'http://{get_ip()}:8001/get_token', headers=headers).json()
    return token['token']


if __name__ == '__main__':
    print(get_token())
