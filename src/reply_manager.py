import abc
import typing as t


class Reply(object):

    # reply base
    def __init__(self, message_data: str):
        self.message_data = message_data

    @abc.abstractmethod
    def reply_type(self):
        return self.reply_type


class CVEInfoDisplayReply(Reply):

    # reply the cve info card to the client
    @staticmethod
    def reply_type():
        return "cve_info_display"


class WeatherDisplayReply(Reply):

    # reply the weather card to the client
    @staticmethod
    def reply_type():
        return "weather_display"


class LeetCodeDailyDisplayReply(Reply):

    # reply the weather card to the client
    @staticmethod
    def reply_type():
        return "leetcode_daily_display"


class GPTGetAnswerReply(Reply):
    # get the answer from xinhuo_gpt

    @staticmethod
    def reply_type():
        return "gpt_get_answer"


class GetBilibiliProgressReply(Reply):
    # get the bilibili favorite videos progress and notice user

    @staticmethod
    def reply_type():
        return "get_bilibili_progress"


class RepeatMessageReply(Reply):
    # repeat the user's message to the client

    @staticmethod
    def reply_type():
        return "repeat_message"


class ReplyManager(object):
    reply_callback_map = dict()
    reply_type_map = dict()

    # the instruction map to the reply_type
    reply_instruction_map = {
        "天气": "weather_display",
        "CVE": "cve_info_display",
        "每日一题": "leetcode_daily_display",
        "提问": "gpt_get_answer",
        # TODO: set_daily_tasks
        "任务": "set_daily_tasks",
        "B站进度": "get_bilibili_progress",
        "其他": "repeat_message"
    }

    # Here need to add new reply handler
    _reply_list = [WeatherDisplayReply, RepeatMessageReply, CVEInfoDisplayReply, LeetCodeDailyDisplayReply,
                   GPTGetAnswerReply, GetBilibiliProgressReply]

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
    def get_handler_with_reply(instruction: str, message_data: str):
        # get reply_type
        reply_type = ReplyManager.reply_instruction_map.get(instruction, "repeat_message")
        print(reply_type)
        # build reply
        reply = ReplyManager.reply_type_map.get(reply_type)(message_data)
        # get handler
        return ReplyManager.reply_callback_map.get(reply_type), reply
