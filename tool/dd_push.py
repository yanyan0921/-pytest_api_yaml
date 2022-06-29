#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/29 
@Author  : LL
@File    : dd_push.py
钉钉推送
'''
import json

import requests

from tool import get_ip
def dd_push(allure_ip):
  HEADERS = {"Content-Type": "application/json;charset=utf-8"}
  # 之前复制的接口地址和token信息
  url = 'https://oapi.dingtalk.com/robot/send?access_token=a3c43eca2320c3f4f3b4daeb8895e9d035327e149c4c70e87c87f073cb65cb93'
  #content里面要设置关键字
  data_info = {
    "msgtype": "text",
    "text": {"content": f'''allure测试报告:\n{allure_ip}'''
    }
    #是否@所有人
    # ,"isAtAll": False
    #这是配置需要@的人
     ,"at": {"atMobiles": ["155xxxx06"]}
  }
  value = json.dumps(data_info)
  response = requests.post(url,data=value,headers=HEADERS)
  if response.json()['errmsg']!='ok':
    print(response.text)

if __name__ == '__main__':
    dd_push(f'http://{get_ip()}:2008/')