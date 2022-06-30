#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/29 
@Author  : LL
@File    : conftest.py
'''
import os
import pytest
from config.config import dd_path

from tool import get_token
from tool.read_file import ReadFile


@pytest.fixture(scope='session', autouse=True)
def session_controller():
    '''全局前置和后置'''
    '''测试开始，写入token信息'''
    token = get_token()
    ReadFile.yaml_write_token(token)
    yield
    '''测试结束发送钉钉'''
    # 这里加等待时间不行，发送钉钉还是在启动报告服务之前
    os.system(f'python {dd_path}')
