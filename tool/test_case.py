#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/15 
@Author  : LL
@File    : test_case.py
'''
import pytest

from tool.allure_ import allure_title, allure_step_no
from tool.case_test import case_assert_result
from tool.log import logger
from tool import ReadFile


@pytest.mark.skipif(ReadFile.check_case_title_is_sole(),reason='用例有重复标题')
@pytest.mark.parametrize('case_data',ReadFile.read_case())
def test_main(case_data:dict):
    case_title = case_data['case_title']
    allure_title(case_title)
    case_file_location = ReadFile.case_file_location(case_data['case_title'])
    logger.info(f'-----开始运行 "{case_title}"用例,该用例属于{case_file_location}文件------')
    allure_step_no(f'该用例属于{case_file_location}文件')
    assert case_assert_result(case_data)
