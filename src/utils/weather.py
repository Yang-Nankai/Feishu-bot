# -*- coding: utf-8 -*-
# @Time    : 2023/11/20 22:59
# @Comment :

import requests
import json
import os
from dotenv import load_dotenv
from Exceptions import WeatherDataException

dotenv_path = os.path.join(os.path.dirname(__file__), '../../', 'config', '.env')
load_dotenv(dotenv_path)

# load from env
DEFAULT_CITY_CODE = os.getenv("DEFAULT_CITY_CODE")


def weather_to_group_table(forecast_data: list) -> list:
    group_data = list()
    for col_data in forecast_data:
        col_json = dict()
        col_json["date"] = col_data["ymd"]
        col_json["temperature"] = col_data["high"] + "/" + col_data["low"]
        col_json["type"] = col_data["type"]
        group_data.append(col_json)

    return group_data[0:3]


def weather_data_handle(weather_data: dict) -> dict:
    template_variables = dict()

    template_variables["group_table"] = weather_to_group_table(weather_data["data"]["forecast"])
    template_variables["area"] = weather_data["cityInfo"]["parent"] + weather_data["cityInfo"]["city"]
    template_variables["update_time"] = weather_data["time"]
    template_variables["humidity"] = str(weather_data["data"]["shidu"])
    template_variables["pm25"] = str(weather_data["data"]["pm25"])
    template_variables["pm10"] = str(weather_data["data"]["pm10"])
    template_variables["now_temperature"] = str(weather_data["data"]["wendu"])
    template_variables["air_quality"] = weather_data["data"]["quality"]
    template_variables["daily_notice"] = weather_data["data"]["ganmao"]

    return  template_variables


def weather_data_content_request(weather_data: dict, card_id: str) -> dict:
    content = dict()
    content["data"] = dict()
    content["type"] = "template"
    content["data"]["template_id"] = card_id
    content["data"]["template_variable"] = weather_data_handle(weather_data)
    return content


def request_weather_data_from_url(weather_url: str, weather_card_id: str, city_code: str) -> str:
    url = '{}{}'.format(weather_url, city_code if city_code is not None else DEFAULT_CITY_CODE)
    res = requests.get(url)
    if res.status_code != 200:
        raise WeatherDataException("No Weather Data.")
    print(res.content.decode('utf-8'))
    weather_data = json.loads(res.content)
    reply_weather_data = weather_data_content_request(weather_data, weather_card_id)
    return json.dumps(reply_weather_data)