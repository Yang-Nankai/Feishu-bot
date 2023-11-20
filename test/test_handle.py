# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 15:48
# @Comment :
def get_content_reply(message: str) -> str:
    # Data in the form of "keywords content". If it is not in
    # this format, the original content will be returned.
    message_list = message.split(' ')  # use the space to split
    instruction = message_list[0] if len(message_list) > 0 else ''
    print(message_list)

get_content_reply("天气 这是什么")