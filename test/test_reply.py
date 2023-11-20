# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 22:24
# @Author  : XXX
# @Software: PyCharm 
# @Comment :

import abc
import typing as t

class Reply(object):

    def __init__(self):
        pass

    @abc.abstractmethod
    def reply_type(self):
        return self.reply_type

class WeatherDisplayReply(Reply):
    # reply the weather card to the client

    @staticmethod
    def reply_type(self):
        return "weather_display"

class RepeatMessageReply(Reply):
    # repeat the user's message to the client

    @staticmethod
    def reply_type(self):
        return "repeat_message"

class ReplyManager(object):
    reply_callback_map = dict()
    reply_type_map = dict()

    # the instruction map to the reply_type
    reply_instruction_map = {
        "天气" : "weather_display",
        "其他" : "repeat_message"
    }

    # Here need to add new reply handler
    _reply_list = []

    def __init__(self):
        for reply in ReplyManager._reply_list:
            ReplyManager.reply_type_map[reply.reply_type()] = reply

    def register(self, reply_type: str) -> t.Callable:
        def decorator(f: t.Callable) -> t.Callable:
            self.register_handler_with_reply_type(reply_type=reply_type, handler=f)
            return f

        return decorator

    @staticmethod
    def register_handler_with_reply_type(reply_type, handler):
        ReplyManager.reply_callback_map[reply_type] = handler

    @staticmethod
    def get_handler_with_reply(instruction: str):
        # get reply_type
        reply_type = ReplyManager.reply_instruction_map.get(instruction, "repeat_message")
        print(reply_type)
        # # build reply
        # reply = ReplyManager.reply_type_map.get(reply_type)()
        # # get handler
        # return ReplyManager.reply_callback_map.get(reply_type), reply
        #


reply_manager = ReplyManager()
reply_manager.get_handler_with_reply("这是")