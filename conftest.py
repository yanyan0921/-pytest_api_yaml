#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/29 
@Author  : LL
@File    : conftest.py
'''
import os

import pytest
from tool.log import logger
from config.config import dd_path
from time import sleep

@pytest.fixture(scope='session',autouse=True)
def session_controller():
    '''全局前置和后置'''
    logger.info('==============================测试开始==============================')
    print()
    yield
    #发送钉钉报告,等待报告服务器先启动，启动需要时间，启动完才发送报告链接（时间自行确定）
    sleep(5)
    os.system(f'python {dd_path}')
    logger.info('==============================测试结束==============================')
