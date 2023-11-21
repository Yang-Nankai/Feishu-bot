# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 15:39
# @Comment :
import json
import os
from dotenv import load_dotenv
from reply import ReplyManager, WeatherDisplayReply, RepeatMessageReply
from weather import request_weather_data_from_url
from utils.city_code import get_city_code_by_region

dotenv_path = os.path.join(os.path.dirname(__file__), '../', 'config', '.env')
load_dotenv(dotenv_path)

# load from env
WEATHER_URL = os.getenv("WEATHER_URL")
WEATHER_CARD_ID = os.getenv("WEATHER_CARD_ID")

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


@reply_manager.register("repeat_message")
def repeat_message_handler(req_data: RepeatMessageReply):
    msg_type = "text"
    return msg_type, str(req_data.message_data)


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
