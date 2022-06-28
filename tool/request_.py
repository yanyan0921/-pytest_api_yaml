#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/10 
@Author  : LL
@File    : request_.py
'''
import json

import requests
from tool import requests_environment_info
from config.config import Environment
from tool.allure_ import allure_description, allure_step_no
from tool.log import logger

class Requests:
    @classmethod
    def get(cls, path):
        url = requests_environment_info(Environment)['ip'] + path
        headers = requests_environment_info(Environment)['headers']
        allure_step_no(f'最终请求地址 {url}')
        logger.info(f'get请求的最终请求地址:{url}')
        result = requests.get(url=url, headers=headers).json()
        logger.info(f'{url}返回结果：{result}')
        return result

    @classmethod
    def post(cls, path, data):
        url = requests_environment_info(Environment)['ip'] + path
        headers = requests_environment_info(Environment)['headers']
        allure_step_no(f'最终请求地址 {url}')
        allure_description(f'请求参数:{data}')
        logger.info(f'post请求的最终请求地址:{url},请求参数{data}')
        result = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
        logger.info(f'{url}返回结果：{result}')
        return result

if __name__ == '__main__':
    Requests.get('/get')
    Requests.post('/post',{'data':'data'})
    # ParameterSetting.parameter_setting({'b': '$.b', 'g': '$.g'})
