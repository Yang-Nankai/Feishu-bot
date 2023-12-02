# -*- coding: utf-8 -*-
# @Time    : 2023/12/2 15:49
# @Comment :

import copy
import json
import requests

from src.utils.Exceptions import BilibiliApiException

FAVORITE_LIST_DETAIL = "/x/v3/fav/resource/list"

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


class BilibiliApiClient(object):
    def __init__(self, bilibili_url, session_data, bilibili_jct):
        self.bilibili_url = bilibili_url
        self.session_data = session_data
        self.bilibili_jct = bilibili_jct

    def favorite_list_detail(self, media_id, pn=1, ps=20) -> dict:
        favorite_detail = "{}{}?media_id={}&pn={}&ps={}&order=mtime&platform=web".format(
            self.bilibili_url, FAVORITE_LIST_DETAIL, media_id, pn, ps
        )
        cookies = {
            "SESSDATA": self.session_data,
            "bili_jct": self.bilibili_jct
        }
        response = requests.get(favorite_detail, headers=headers, cookies=cookies)
        res_text = response.text
        if res_text is not None:
            res_dict = json.loads(res_text)

        favorite_info = self.favorite_res_to_info(res_dict)
        return res_dict

    def favorite_res_to_info(self, res_dict: dict) -> dict:
        favorite_info = copy.deepcopy(FAVORITE_INFO_TEMPLATE)
        res_code = res_dict["code"]
        if res_code != 0:
            raise BilibiliApiException("Code Not Success!")  # Here need to show the problem
        if res_dict is not None and res_code == 0:
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
                media_info["completed_progress"] = "56"
                favorite_info["group_table"].append(media_info)
        return favorite_info

    @staticmethod
    def format_duration(duration: int) -> str:
        hours, remainder = divmod(duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        # 使用字符串格式化进行填充零位
        time_str = "{:02d}:{:02d}:{:02d}".format(int(hours), int(minutes), int(seconds))

        return time_str
