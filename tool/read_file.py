#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@time    : 2022/6/10
@Author  : LL
@File    : read_file.py
'''
from pathlib import Path
from tool.log import logger
import yaml
from config.config import exclude_file, exclude_dir, Environment
from tool.mysql_ import mysql_db
import os


class ReadFile:
    project_directory = str(Path(__file__).parent.parent) + '/'

    @classmethod
    def read_yaml(cls, path):
        '''读取yaml文件，以字典格式返回{'用例标题':{'path':'/test','data':{'id':1}}}'''
        path = cls.project_directory + path
        file = open(path, 'r', encoding='utf-8')
        with file as doc:
            content = yaml.load(doc, Loader=yaml.Loader)
            return content

    @classmethod
    def yaml_write_token(cls, token):
        environment_path = 'config/environment.yaml'
        # 把配置先文件读出来
        environment = cls.read_yaml(environment_path)
        # 把token赋值给对应的环境信息
        environment[Environment]['headers']['token'] = token
        # 重写写入环境信息,这里之所以用这个cls.project_directory，应该read_yaml这个方法里面有，但是这个没有
        with open(cls.project_directory + environment_path, "w", encoding="utf-8") as f:
            yaml.dump(environment, f)

    @classmethod
    def read_case(cls):
        '''读取case下需要执行的用例文件并返回用例数据'''
        path_list = cls.file_execute_list()
        case_data = {}
        for i in path_list:
            case_data.update(cls.read_yaml(i))
        logger.info(f'最终执行的用例数据:{case_data}')
        for k, v in case_data.items():
            case_name = k
            if v['is_run'] == True:
                v['case_title'] = case_name
                if v['precondition_sql'] != None:
                    for i in v['precondition_sql']:
                        mysql_db.execute_db(i)
                if v['data'] != None:
                    sql_k_list = []
                    sql_v_list = []
                    for data_k, data_v in v['data'].items():
                        if 'sql-' in data_v:
                            sql_k_list.append(data_k)
                            sql_result = mysql_db.select_db(data_v[4:])
                            sql_v_list.append(sql_result)
                    new_v = dict(zip(sql_k_list, sql_v_list))
                    v['data'].update(new_v)
                yield v

    @classmethod
    def file_execute_list(cls, exclude_file=exclude_file, exclude_dir=exclude_dir):
        '''
        :param exclude_dir: 要排除的目录（二级目录）例子：ctms  list格式
        :param exclude_file: 要排除的文件（case目录下所有文件）例子：case/ctms/test.yaml   case/waybill.yaml list格式
        :return: 获取case下的所有用例文件列表,最多支持二级目录,通用排除文件返回最终要执行的用例文件
        '''
        file_list = []
        case_path = cls.project_directory + 'case'
        for filename in os.listdir(case_path):
            if 'yaml' in filename:
                file_list.append('case/' + filename)
            else:
                for i in os.listdir(case_path + '/' + filename):
                    if filename in exclude_dir:
                        continue
                    file_list.append('case/' + filename + '/' + i)
        if exclude_file != []:
            for i in exclude_file:
                file_list.remove(i)
        return file_list

    @classmethod
    def case_file_location(cls, case_title):
        '''
        :param case_name: 用例名称
        :return: 判断这个用例名称是不是在哪一个文件里面（前提用例名称唯一），返回文件名（含路径）
        '''
        path_list = cls.file_execute_list()
        for i in path_list:
            if case_title in cls.read_yaml(i).keys():
                return i

    @classmethod
    def check_case_title_is_sole(cls):
        '''
        :return: 检查是否有重复的用例名称，放到全局前置,True就是有重复的，False就是没有
        '''
        from collections import Counter
        execute_list = cls.file_execute_list()
        case_title_list = []
        for i in execute_list:
            case_dict = cls.read_yaml(i)
            case_key_list = [i for i in case_dict.keys()]
            case_title_list += case_key_list
        b = dict(Counter(case_title_list))
        repetition = {key: value for key, value in b.items() if value > 1}
        if bool(repetition):
            logger.error(f'有重复的用例标题，请检查所有要执行的用例文件，重复标题和重复次数{repetition}')
            return True
        else:
            return False


if __name__ == '__main__':
    ReadFile.file_execute_list([], ['c', 'ctms'])
    # 路径使用读取文件的相对路径
    # 读取环境配置文件测试
    # print(ReadFile.read_yaml('config/environment.yaml'))
    # 读取用例文件测试
    # case_data = ReadFile.read_yaml('case/test.yaml')
    # print(case_data)
    # 测试用例数据生成器返回
    # case_list=ReadFile.read_case()
    # for i in case_list:
    #     print(i)
