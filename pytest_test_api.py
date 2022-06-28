#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/21 
@Author  : LL
@File    : pytest_test_api.py
实现mock功能：
    token拦截
    获取token(需要token把写入yaml)
    2个业务流程
    接口参数依赖校验
下载相关依赖包 需要python3.6以上版本
pip install fastapi[all]
'''

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel


def get_ip():
    '''获取本机ip地址'''
    import socket
    res = socket.gethostbyname(socket.gethostname())
    return res


def verify_token(token: str = Header(...)):
    if token != "em123dca666333":
        raise HTTPException(status_code=400, detail="Token 无效")


# 全局依赖
app = FastAPI(dependencies=[Depends(verify_token)])


@app.get("/get_token")
def get_token(token: str = Header(...)):
    '''获取token信息'''
    return {'token': token}

'''获取运单号'''
'''测试需要保存运单号'''
@app.get('/get_waybill_no')
def get_waybill_no():
    return {'waybill_no': 'lj520'}


class WaybillNo(BaseModel):
    waybill_no: str
    lu_dan_ren: str

'''录单'''
'''测试需要使用运单号'''
@app.post('/lu_dan', status_code=status.HTTP_201_CREATED)
def lu_dan(waybill: WaybillNo):
    if waybill.waybill_no != 'lj520':
        raise HTTPException(status_code=400, detail='运单号格式错误')
    return {'msg': '运单创建成功', 'waybill_info': waybill}


'''创建账单'''
'''测试需要保存账单号和创建人'''
class CreateBill(BaseModel):
    create_month: str
    create_name: str



@app.post('/create_bill')
def create_bill(bill: CreateBill):
    return {'bill_no': 'lj1314', 'bill_info': bill}


'''确认账单'''
'''测试需要使用账单号，需要保存确认人'''
class AffirmBill(BaseModel):
    affirm_name: str
    bill_no: str


@app.post('/affirm_bill')
def affirm_bill(bill: AffirmBill):
    if bill.bill_no != 'lj1314':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账单不存在')
    return {'bill_no': bill.bill_no, 'bill_info': bill}


'''核销账单'''
'''测试需要使用账单号、创建人和确认人'''
class WriteOffBill(BaseModel):
    create_name: str
    affirm_name: str
    bill_no: str


@app.post('/write_off_bill')
def write_off_bill(bill: WriteOffBill):
    if bill.bill_no != 'lj1314':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='账单不存在')
    if bill.create_name != bill.affirm_name:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='创建人和确认人不一致')
    return {'bill_no': bill.bill_no, 'bill_info': bill}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='pytest_test_api:app', host=get_ip(), port=8001, reload=True, debug=True)
