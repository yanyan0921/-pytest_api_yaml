#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/15 
@Author  : LL
@File    : test_case.py
'''
import pytest

from tool.allure_ import allure_title
from tool.case_test import case_assert_result
from tool.log import logger
from tool import ReadFile



@pytest.mark.parametrize('case_data',ReadFile.read_case())
def test_main(case_data:dict):
    case_title = case_data['case_title']
    allure_title(case_title)
    logger.info(f'-----开始运行 "{case_title}"用例------')
    assert case_assert_result(case_data)
