# -*- coding: utf-8 -*-
# @Time    : 2023/12/2 15:49
# @Comment : Bilibili API Client

import copy
import itertools
import json
import re
import requests

from src.utils.Exceptions import BilibiliApiException

FAVORITE_LIST_DETAIL_URL = "/x/v3/fav/resource/list"

headers = {
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


class BilibiliApiClient:
    def __init__(self, bilibili_url, bilibili_api_url, session_data, bilibili_jct):
        self.bilibili_url = bilibili_url
        self.bilibili_api_url = bilibili_api_url
        self.session_data = session_data
        self.bilibili_jct = bilibili_jct

    @property
    def get_cookies(self) -> dict:
        return {"SESSDATA": self.session_data, "bili_jct": self.bilibili_jct}

    def all_favorite_info(self, media_id: str) -> dict:
        all_res_dict = []
        for index in itertools.count(1):
            res_dict = self._favorite_list_detail(media_id, index)
            if not res_dict["data"]["has_more"]:
                break
            all_res_dict.append(res_dict)
        return self.all_favorite_res_to_info(all_res_dict)

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
            self.bilibili_api_url, FAVORITE_LIST_DETAIL_URL, media_id, pn, ps
        )
        response = requests.get(favorite_detail, headers=headers, cookies=self.get_cookies)
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
                media_info["video_image"] = media_item["cover"]
                media_info["video_sets"] = media_item["page"]
                media_info["completed_progress"] = self.get_video_completed_progress(media_item["bvid"],
                                                                                     media_item["duration"])
                favorite_info["group_table"].append(media_info)
        return favorite_info

    def get_video_completed_progress(self, bvid: str, duration: int) -> str:
        """
        :param bvid: the bvid of a video
        :param duration: the total time of a video

        :return: the completed progress of the video
        """
        bvid_url = f"{self.bilibili_url}video/{bvid}"

        resp = requests.get(bvid_url, headers=headers, cookies=self.get_cookies)

        try:
            play_info = re.findall(r'<script>window.__playinfo__=(.*?)</script>', resp.text)[0]
            play_json = json.loads(play_info)
            last_play_time = play_json["data"]["last_play_time"]
            completed_progress = "{:.3}".format(last_play_time / 1000 / duration * 100)  # 保留三位有效数字
        except Exception as e:
            completed_progress = 0
            # 存在已经失效的视频
            print("存在已失效的视频")

        return completed_progress

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

    # 去清除所有已经失效的视频
    def remove_all_
