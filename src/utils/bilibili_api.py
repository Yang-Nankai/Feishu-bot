# -*- coding: utf-8 -*-
# @Time    : 2023/12/2 15:49
# @Comment : Bilibili API Client

import copy
import itertools
import json
import os
import re
import requests
from dotenv import load_dotenv
from src.api import MessageApiClient
from src.utils.Exceptions import BilibiliApiException

dotenv_path = os.path.join(os.path.dirname(__file__), '../', 'config', '.env')
load_dotenv(dotenv_path)

# global variables
BILIBILI_URL = "https://www.bilibili.com"
BILIBILI_API_URL = "https://api.bilibili.com"
FAVORITE_LIST_DETAIL_URL = "/x/v3/fav/resource/list"
FAVORITE_CLEAN_URL = "/x/v3/fav/resource/clean"
MOVE_VIDEO_URL = "/x/v3/fav/resource/move"
FINISHED_PERCENT = 95  # 设置视频看完的阈值

# load from env
SESSDATA = os.getenv("SESSDATA")
BILIBILI_JCT = os.getenv("BILIBILI_JCT")
FAVORITE_ID = os.getenv("FAVORITE_ID")
FINISHED_FAVORITE_ID = os.getenv("FINISHED_FAVORITE_ID")
USER_ID = os.getenv("USER_ID")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
LARK_HOST = os.getenv("LARK_HOST")

# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)

HEADER = {
    "Referer": "https://www.bilibili.com/",
    "Origin": "https://space.bilibili.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 "
                  "Safari/537.36 Edg/119.0.0.0"
}

FAVORITE_INFO_TEMPLATE = {
    "favorite_name": str(),
    "uncompleted_quantity": str(),
    "group_table": list()
}

MEDIA_INFO_TEMPLATE = {
    "video_name": str(),
    "video_url": str(),
    "video_author": str(),
    "video_detail": str(),
    "video_time": str(),
    "video_image": str(),
    "video_sets": str(),
    "completed_progress": str()
}


def request_bilibili_progress_data(card_id: str) -> str:

    bilibili_api_client = BilibiliApiClient(SESSDATA, BILIBILI_JCT)

    # 首先得清除一下失效的视频
    is_cleaned = bilibili_api_client.remove_expired_videos(FAVORITE_ID)
    if is_cleaned:
        print("Clean Successfully!")

    # 然后得到发送消息需要的Info
    progress_info = bilibili_api_client.all_favorite_info(FAVORITE_ID)

    # 然后组装发送的content
    content = dict()
    content["data"] = dict()
    content["type"] = "template"
    content["data"]["template_id"] = card_id
    content["data"]["template_variable"] = progress_info

    return json.dumps(content)


class BilibiliApiClient:
    def __init__(self, session_data, bilibili_jct):
        self.session_data = session_data
        self.bilibili_jct = bilibili_jct

    @property
    def get_cookies(self) -> dict:
        return {"SESSDATA": self.session_data, "bili_jct": self.bilibili_jct}

    def all_favorite_info(self, media_id: str) -> dict:
        all_res_list = self.all_favorite_list_detail(media_id)
        return self.all_favorite_res_to_info(all_res_list)

    def all_favorite_list_detail(self, media_id: str) -> list:
        """
        get all videos detail of a favorite
        :param media_id: the favorite id
        :return: all videos detail of the favorite
        """
        all_res_dict = list()
        for index in itertools.count(1):
            res_dict = self._favorite_list_detail(media_id, index)
            all_res_dict.append(res_dict)
            if not res_dict["data"]["has_more"]:
                break
        return all_res_dict

    def all_favorite_res_to_info(self, all_res: list) -> dict:
        all_favorite_info = copy.deepcopy(FAVORITE_INFO_TEMPLATE)
        for favorite_res_item in all_res:
            favorite_info = self.favorite_res_to_info(favorite_res_item)
            self._add_favorite_info_dict(all_favorite_info, favorite_info)
        return all_favorite_info

    @staticmethod
    def _add_favorite_info_dict(first_favorite_info: FAVORITE_INFO_TEMPLATE,
                                second_favorite_info: FAVORITE_INFO_TEMPLATE) -> FAVORITE_INFO_TEMPLATE:
        first_favorite_info["favorite_name"] = second_favorite_info["favorite_name"]
        first_favorite_info["uncompleted_quantity"] = second_favorite_info["uncompleted_quantity"]
        first_favorite_info["group_table"].extend(second_favorite_info["group_table"])
        return first_favorite_info

    def _favorite_list_detail(self, media_id, pn=1, ps=20) -> dict:
        """
        :param media_id: the video id
        :param pn: the start page
        :param ps: the num of page video

        :return: the favorite list 'all' information
        """
        favorite_detail = "{}{}?media_id={}&pn={}&ps={}&order=mtime&platform=web".format(
            BILIBILI_API_URL, FAVORITE_LIST_DETAIL_URL, media_id, pn, ps
        )
        response = requests.get(favorite_detail, headers=HEADER, cookies=self.get_cookies)
        res_dict = json.loads(response.text) if response.text else {}
        return res_dict

    def favorite_res_to_info(self, res_dict: dict) -> dict:
        """
        :param res_dict: the favorite all information

        :return: the favorite information that we 'need'
        """
        favorite_info = copy.deepcopy(FAVORITE_INFO_TEMPLATE)
        res_code = res_dict["code"]
        if res_code != 0:
            raise BilibiliApiException("Code Not Success!")  # Here need to show the problem
        if res_dict and res_code == 0:
            favorite_info["favorite_name"] = res_dict["data"]["info"]["title"]
            favorite_info["uncompleted_quantity"] = res_dict["data"]["info"]["media_count"]
            for media_item in res_dict["data"]["medias"]:
                media_info = copy.deepcopy(MEDIA_INFO_TEMPLATE)
                media_info["video_name"] = media_item["title"]
                media_info["video_url"] = "https://www.bilibili.com/video/" + media_item["bvid"] + "/"
                media_info["video_author"] = media_item["upper"]["name"]
                media_info["video_detail"] = media_item["intro"]
                media_info["video_time"] = self.format_duration(media_item["duration"])
                media_info["video_image"] = message_api_client.upload_image_from_url(media_item["cover"])
                media_info["video_sets"] = media_item["page"]
                media_info["completed_progress"] = self.get_video_completed_progress(media_item["id"], media_item["bvid"],
                                                                                     media_item["duration"])
                favorite_info["group_table"].append(media_info)
        return favorite_info

    def get_video_completed_progress(self, bid: str, bvid: str, duration: int) -> str:
        """
        :param bvid: the bvid of a video
        :param duration: the total time of a video

        :return: the completed progress of the video
        """
        bvid_url = f"{BILIBILI_URL}/video/{bvid}"

        resp = requests.get(bvid_url, headers=HEADER, cookies=self.get_cookies)

        try:

            play_info = re.findall(r'<script>window.__playinfo__=(.*?)</script>', resp.text)[0]
            play_json = json.loads(play_info)
            last_play_time = play_json["data"]["last_play_time"]

            completed_progress = last_play_time / 1000 / duration * 100
            str_completed_progress = "{:.3}".format(completed_progress)  # 保留三位有效数字

            print("progress:", completed_progress)
            # 如果视频看完了，则移动视频到 已完成 收藏夹
            if completed_progress > FINISHED_PERCENT:  # 这里设置阈值大于95则代表看得差不多了
                self.move_video_favorite(FAVORITE_ID, FINISHED_FAVORITE_ID, USER_ID, [bid])

        except Exception as e:
            completed_progress = 0
            # 存在已经失效的视频
            print("Exists expired video")

        return str_completed_progress

    @staticmethod
    def format_duration(duration: int) -> str:
        """
        :param duration: the time of a vedio
        :return: time format like "00:30:12"
        """
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        # 使用字符串格式化进行填充零位
        time_str = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

        return time_str

    def remove_expired_videos(self, media_id: str) -> bool:
        """
        Remove all expired videos from this function
        :param media_id: the favorite id
        :return: bool, True if remove successfully and False if unsuccessfully
        """
        clean_url = f"{BILIBILI_API_URL}{FAVORITE_CLEAN_URL}"
        params = {"media_id": media_id, "csrf": self.bilibili_jct}

        try:
            resp = requests.post(clean_url, params=params, cookies=self.get_cookies, headers=HEADER)
            resp_info = resp.json()

            if resp_info["code"] == 0:
                return True
            else:
                raise BilibiliApiException("Clean Not Success!")

        except Exception as e:
            print(f"An error occurred: {e}")

        return False

    def move_video_favorite(self, src_media_id: str, tar_media_id: str, mid: str, video_ids: list) -> bool:
        """
        Move a video from one favorite to another favorite
        :param src_media_id: source favorite id
        :param tar_media_id: target favorite id
        :param mid: user id
        :param video_ids: video ids like: ["123456", "234567"]
        :return: True or False
        """
        move_url = f"{BILIBILI_API_URL}{MOVE_VIDEO_URL}"
        # 这里类型均设置为了2，考虑到没有音频类型，均为视频类型(1是音频，2是视频，21是视频合集)
        resources = ', '.join([f'{id}:2' for id in video_ids])
        params = {"src_media_id": src_media_id, "tar_media_id": tar_media_id, "mid": mid, "resources": resources, "csrf": self.bilibili_jct}

        try:
            resp = requests.post(move_url, params=params, cookies=self.get_cookies, headers=HEADER)
            resp_info = resp.json()

            if resp_info["code"] == 0:
                print(f"Finished the {resources} videos!")
                return True
            else:
                raise BilibiliApiException("Move Not Success!")

        except Exception as e:
            print(f"An error occurred: {e}")

        return False




