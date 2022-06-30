#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/15
@Author  : LL
@File    : assert_.py
断言格式 ["'12' in '123'", '"ig" == "$.ig"', '1==1']
'''
from jsonpath import jsonpath

from tool.allure_ import allure_step_no
from tool.log import logger
from tool.mysql_ import mysql_db


class Assert:
    @classmethod
    def assert_response(cls, assert_list: list, api_response: dict):
        new_assert_list = []
        for i in assert_list:
            if '$.' in i:
                wz = i.find('$')
                json_path = i[wz:len(i) - 1]
                value = jsonpath(api_response, json_path)
                if not value:
                    logger.error(f'断言表达式提取失败，请检查，接口返回结果{api_response}，表达式{json_path}')
                    return False
                value = value[0]
                i = i.replace(json_path, value)
            if 'sql-' in i:
                wz = i.find('-')
                sql = i[wz + 1:len(i) - 1]
                i = i.replace('sql-' + sql, mysql_db.select_db(sql))
            new_assert_list.append(i)
        allure_step_no(f'断言列表：{new_assert_list}')
        logger.info(f'断言表达式新列表：{new_assert_list}')
        assert_result_list = []
        for i in new_assert_list:
            assert_result = eval(i)
            assert_result_list.append(assert_result)
        # logger.info(f'断言结果列表:{assert_result_list}')
        if False in assert_result_list:
            return False
        return True


if __name__ == '__main__':
    print(Assert.assert_response(["'12' in '123'", '"ig" == "$.ig"', '1==1'], {'id': 1, 'ig': 'TheShy'}))
