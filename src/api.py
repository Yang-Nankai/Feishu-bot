#! /usr/bin/env python3.8
import json
import os
import logging
import requests
from io import BytesIO
from requests_toolbelt import MultipartEncoder
from src.utils.Exceptions import LarkException

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

# const
TENANT_ACCESS_TOKEN_URI = "/open-apis/auth/v3/tenant_access_token/internal"
MESSAGE_URI = "/open-apis/im/v1/messages"
UPLOAD_IMAGE_URL = "/open-apis/im/v1/images"


class MessageApiClient(object):
    def __init__(self, app_id, app_secret, lark_host):
        self._app_id = app_id
        self._app_secret = app_secret
        self._lark_host = lark_host
        self._tenant_access_token = ""

    @property
    def tenant_access_token(self):
        return self._tenant_access_token

    def upload_image_from_url(self, img_url: str) -> str:
        """
        upload image use url and has a default img_key if not success
        :param img_url: the image url which want to upload
        :return: img_key
        """
        # Update the authorized tenant access token
        self._authorize_tenant_access_token()

        # default image key
        default_img_key = "img_v2_a4b2d72a-211b-440b-8950-880066cfbabg"

        url = "{}{}".format(
            self._lark_host, UPLOAD_IMAGE_URL
        )

        # Download image from url
        image_response = requests.get(img_url)
        if image_response.status_code == 200:
            image_content = BytesIO(image_response.content)

            # build form dictionary
            form = {'image_type': 'message', 'image': ('image.jpg', image_content, 'image/jpeg')}

            # create MultipartEncoder
            multi_form = MultipartEncoder(form)

            # set headers
            headers = {
                'Authorization': 'Bearer ' + self.tenant_access_token,
                'Content-Type': multi_form.content_type
            }

            response = requests.request("POST", url, headers=headers, data=multi_form)

            print(response.headers['X-Tt-Logid'])  # for debug or oncall
            # print(response.content)  # Print Response
            resp_json = json.loads(response.content)

            # If code is 0 represents success
            if resp_json["code"] == 0:
                return resp_json["data"]["image_key"]

        return default_img_key

    def send_text_with_open_id(self, open_id, content, msg_type):
        self.send("open_id", open_id, msg_type, content)

    def send(self, receive_id_type, receive_id, msg_type, content):
        # send message to user, implemented based on Feishu open api capability. doc link:
        # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create
        self._authorize_tenant_access_token()
        url = "{}{}?receive_id_type={}".format(
            self._lark_host, MESSAGE_URI, receive_id_type
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.tenant_access_token,
        }

        req_body = {
            "receive_id": receive_id,
            "content": content,
            "msg_type": msg_type,
        }
        resp = requests.post(url=url, headers=headers, json=req_body)
        MessageApiClient._check_error_response(resp)

    def _authorize_tenant_access_token(self):
        # get tenant_access_token and set, implemented based on Feishu open api capability. doc link:
        # https://open.feishu.cn/document/ukTMukTMukTM/ukDNz4SO0MjL5QzM/auth-v3/auth/tenant_access_token_internal
        url = "{}{}".format(self._lark_host, TENANT_ACCESS_TOKEN_URI)
        req_body = {"app_id": self._app_id, "app_secret": self._app_secret}
        response = requests.post(url, req_body)
        MessageApiClient._check_error_response(response)
        self._tenant_access_token = response.json().get("tenant_access_token")

    @staticmethod
    def _check_error_response(resp):
        # check if the response contains error information
        if resp.status_code != 200:
            resp.raise_for_status()
        response_dict = resp.json()
        code = response_dict.get("code", -1)
        if code != 0:
            logging.error(response_dict)
            raise LarkException(code=code, msg=response_dict.get("msg"))
