# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 20:44
# @Comment :

from datetime import datetime

# 假设 jsonText 是一个包含 topicTags 列表的字典
jsonText = {
    'topicTags': [
        {'name': 'Tag1'},
        {'name': 'Tag2'},
        {'name': 'Tag3'}
        # ... 其他元素
    ]
}

# 使用列表推导式获取每个元素的第二个元素的 'name' 属性
result = [element['name'] for element in jsonText.get('topicTags', [])]

print(result)

date_time = datetime.today().date().__str__()
print(date_time)