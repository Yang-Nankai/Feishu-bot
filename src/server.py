#!/usr/bin/env python3.8

import os
import logging
import requests
from api import MessageApiClient
from event_manager import MessageReceiveEvent, UrlVerificationEvent, EventManager
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from reply_handle import get_content_reply
from data_handle import create_database


# load env parameters form file named .env
# load_dotenv(find_dotenv())
dotenv_path = os.path.join(os.path.dirname(__file__), '../', 'config', '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")

# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
event_manager = EventManager()


def load_config():
    # create database
    create_database()


@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if message.message_type != "text":
        logging.warn("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id
    msg_type, text_content = get_content_reply(message.content)
    # text_content = message.content
    # echo text message
    message_api_client.send_text_with_open_id(open_id, text_content, msg_type)
    return jsonify()

@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)

    return event_handler(event)


# CVE Info API
@app.route("/cve_info", methods=["get"])
def get_daily_cve_info_handler():
    # send messsage to the user
    '''
    open_id: param, the user id need to send
    '''
    open_id = request.args['open_id']
    message_content = '{"text":"CVE"}'
    msg_type, text_content = get_content_reply(message_content)
    message_api_client.send_text_with_open_id(open_id, text_content, msg_type)
    return jsonify()


if __name__ == "__main__":
    # create databse, laod config
    load_config()
    # init()
    app.run(host="0.0.0.0", port=3000, debug=True)
