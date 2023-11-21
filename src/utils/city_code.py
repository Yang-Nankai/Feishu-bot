# -*- coding: utf-8 -*-
# @Time    : 2023/11/21 12:27
# @Comment :

from .city_code_loader import city_data

def get_city_code_by_region(region: str) -> str:
    for city_info in city_data:
        if city_info['region'] == region:
            return city_info['city_code']
    return None