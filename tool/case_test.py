#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/15 
@Author  : LL
@File    : case_test.py
'''
from tool.allure_ import allure_description
from tool.assert_ import Assert
from tool.parameter_setting import ParameterSetting
from tool.request_ import Requests
from tool.log import logger

def replace_(extract_key,api_response):
    '''参数提取处理'''
    logger.info(f'提取参数字典{extract_key}')
    if extract_key:
        extract_value = ParameterSetting.extract_value(api_response, extract_key)
        ParameterSetting.parameter_setting(extract_value, 'save')

def case_assert_result(case_data):
    '''
    :param case_data: yaml读出来的用例数据
    :return:
    get请求暂时没有写参数依赖
    '''
    allure_description(case_data['remark'])
    logger.info(f'用例原始数据：{case_data}')
    if case_data['method'] == 'get':
        api_response = Requests.get(case_data['path'])
        extract_key = case_data['extract_key']
        replace_(extract_key, api_response)
        assert_result = Assert.assert_response(case_data['assert_expression'], api_response)

    elif case_data['method'] == 'post':
        '''参数替换和参数依赖操作必须在一个页面里面，不然页面切换参数池会重置为{}'''
        if ParameterSetting.data_is_replace(case_data['data']):
            data = ParameterSetting.parameter_setting(case_data['data'],'get')
        else:
            data = case_data['data']
        api_response = Requests.post(case_data['path'], data)
        extract_key = case_data['extract_key']
        replace_(extract_key,api_response)
        assert_result = Assert.assert_response(case_data['assert_expression'], api_response)
    else:
        assert_result = False
    case_title = case_data['case_title']
    logger.info(f'-----"{case_title}"用例运行完成------')
    return assert_result
