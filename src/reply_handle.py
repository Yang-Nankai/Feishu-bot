# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 15:39
# @Comment :
import json
import os
from dotenv import load_dotenv
from reply_manager import ReplyManager, WeatherDisplayReply, RepeatMessageReply, CVEInfoDisplayReply, \
                          LeetCodeDailyDisplayReply, GPTGetAnswerReply
from weather import request_weather_data_from_url
from utils.city_code import get_city_code_by_region
from cve_info import request_cve_info_from_url
from leetcode_daily import request_leetcode_daily_from_url
from src.xinhuo_big_model.spark_gpt import SparkGPT

dotenv_path = os.path.join(os.path.dirname(__file__), '../', 'config', '.env')
load_dotenv(dotenv_path)

# load from env
WEATHER_URL = os.getenv("WEATHER_URL")
WEATHER_CARD_ID = os.getenv("WEATHER_CARD_ID")
CVE_CARD_ID = os.getenv("CVE_CARD_ID")
CVE_URL = os.getenv("CVE_URL")
LEETCODE_URL = os.getenv("LEETCODE_URL")
LEETCODE_DAILY_CARD_ID = os.getenv("LEETCODE_DAILY_CARD_ID")
XH_APP_ID = os.getenv("XH_APP_ID")
XH_API_SECRET = os.getenv("XH_API_SECRET")
XH_API_KEY = os.getenv("XH_API_KEY")

# init service
reply_manager = ReplyManager()


@reply_manager.register("weather_display")
def weather_display_handler(req_data: WeatherDisplayReply):
    message_list = get_message_list(req_data.message_data)
    region = message_list[1] if len(message_list) > 1 else ''
    # Here need to do something adjust, and the function should have the exception handle
    city_code = get_city_code_by_region(region)
    msg_type = "interactive"
    weather_data = request_weather_data_from_url(WEATHER_URL, WEATHER_CARD_ID, city_code)
    return msg_type, weather_data


@reply_manager.register("cve_info_display")
def cve_info_display_handler(req_data: CVEInfoDisplayReply):
    msg_type = "interactive"
    cve_info_data = request_cve_info_from_url(CVE_URL, CVE_CARD_ID)
    return msg_type, cve_info_data


@reply_manager.register("repeat_message")
def repeat_message_handler(req_data: RepeatMessageReply):
    msg_type = "text"
    return msg_type, str(req_data.message_data)


@reply_manager.register("leetcode_daily_display")
def leetcode_daily_display_handler(req_data: LeetCodeDailyDisplayReply):
    msg_type = "interactive"
    leetcode_daily_data = request_leetcode_daily_from_url(LEETCODE_URL, LEETCODE_DAILY_CARD_ID)
    return msg_type, leetcode_daily_data


@reply_manager.register("gpt_get_answer")
def gpt_get_answer_handler(req_data: GPTGetAnswerReply):
    msg_type = "text"
    question = str(json.loads(req_data.message_data).get('text'))[2:]  # delete the "提问 "
    speak = SparkGPT(app_id=XH_APP_ID, api_key=XH_API_KEY, api_secret=XH_API_SECRET, domain="generalv3", spark_url="ws://spark-api.xf-yun.com/v3.1/chat", prompt="回答我的问题")
    gpt_answer_data = speak.ask(question)
    print(gpt_answer_data)
    return msg_type, json.dumps({"text": str(gpt_answer_data)})


def get_message_list(message: str) -> dict:
    message_data = json.loads(message)["text"]
    message_list = message_data.split(' ')  # use the space to split
    return message_list


# Return the right reply according to the message
def get_content_reply(message: str):
    # Data in the form of "keywords content". If it is not in
    # this format, the original content will be returned.
    message_list = get_message_list(message)
    print(message_list)
    instruction = message_list[0] if len(message_list) > 0 else '其他'
    print(instruction)
    # choose the funtion according to the instruction
    reply_handler, reply = reply_manager.get_handler_with_reply(instruction, message)

    return reply_handler(reply)
