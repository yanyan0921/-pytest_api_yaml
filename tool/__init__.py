#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config.config import Environment
from tool.read_file import ReadFile


def requests_environment_info(environment=Environment):
    '''
    :param environment: test or pro 测试或者生产环境
    :return: 返回ip和headers信息
    '''
    #配置文件信息
    env_info = ReadFile.read_yaml('config/environment.yaml')
    if environment == 'test':
        #test_environment 测试环境配置文件相关信息
        request_info = env_info['test_environment']
        return {'ip': request_info['http'] + request_info['domain_name'], 'headers': request_info['headers']}
    elif environment == 'pro':
        # pro_environment 生产环境配置文件相关信息
        request_info = env_info['pro_environment']
        return {'ip': request_info['http'] + request_info['domain_name'], 'headers': request_info['headers']}
    else:
        print('暂时只有test和pro环境')


