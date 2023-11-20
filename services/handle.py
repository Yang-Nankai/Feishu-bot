# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 15:39
# @Comment :
import json
import os
from dotenv import load_dotenv
from reply import ReplyManager, WeatherDisplayReply, RepeatMessageReply
from weather import request_weather_data_from_url

dotenv_path = os.path.join(os.path.dirname(__file__), '../', 'config', '.env')
load_dotenv(dotenv_path)

# load from env
WEATHER_URL = os.getenv("WEATHER_URL")
WEATHER_CARD_ID = os.getenv("WEATHER_CARD_ID")

# init service
reply_manager = ReplyManager()


@reply_manager.register("weather_display")
def weather_display_handler(req_data: WeatherDisplayReply):
    print(req_data.message_data)
    msg_type = "interactive"
    weather_data = request_weather_data_from_url(WEATHER_URL, WEATHER_CARD_ID)
    return msg_type, weather_data


@reply_manager.register("repeat_message")
def repeat_message_handler(req_data: RepeatMessageReply):
    msg_type = "text"
    return msg_type, str(req_data.message_data)


# Return the right reply according to the message
def get_content_reply(message: str):
    # Data in the form of "keywords content". If it is not in
    # this format, the original content will be returned.
    message_data = json.loads(message)["text"]
    message_list = message_data.split(' ')  # use the space to split
    instruction = message_list[0] if len(message_list) > 0 else '其他'
    print(instruction)
    # choose the funtion according to the instruction
    reply_handler, reply = reply_manager.get_handler_with_reply(instruction, message)

    return reply_handler(reply)
