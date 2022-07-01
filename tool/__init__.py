#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from config.config import Environment
from tool.read_file import ReadFile


def get_ip():
    '''获取本机ip地址'''
    import socket
    res = socket.gethostbyname(socket.gethostname())
    return res


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
