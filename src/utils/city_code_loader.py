# -*- coding: utf-8 -*-
# @Time    : 2023/11/21 12:04
# @Comment :


import json
import os.path

file_path = os.path.join(os.path.dirname(__file__), '../../', 'data', 'city_code.json')

def load_city_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


# 在模块加载时执行加载数据的操作
city_data = load_city_data(file_path)

