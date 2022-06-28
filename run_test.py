#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/15
@Author  : LL
@File    : run_test.py
'''
import pytest
import os
import shutil
if __name__ == '__main__':

    try:
        # 删除之前的文件夹
        shutil.rmtree("report")
        print('清除之前报告')
    except:
        pass
    pytest.main([])
    # 直接生成报告html文件
    # os.system('allure generate  report/data -o report/html --clean')
    # 编译报告原文件并启动报告服务
    os.system('allure serve report/data')


