# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 20:51
# @Comment :

# -*- coding: utf-8 -*-
# @Comment :

import requests
import json
from datetime import datetime
from Exceptions import LeetCodeDailyException


def get_daily_title_from_json(data: str) -> str:
    try:
        res_data = json.loads(data)
        return res_data.get('data').get('todayRecord')[0].get("question").get('questionTitleSlug')
    except Exception:
        raise LeetCodeDailyException("get_daily_title_from_json has something wrong!")


def get_title_request(leetcode_url: str) -> str:
    try:
        json_data = {
            "operationName": "questionOfToday",
            "variables": {},
            "query": "query questionOfToday { todayRecord {   question {     questionFrontendId     questionTitleSlug"
                     "__typename   }   lastSubmission {     id     __typename   }   date   userStatus   __typename }}"
        }
        res = requests.post(leetcode_url + "/graphql", json=json_data)
    except Exception:
        raise LeetCodeDailyException("get_title_request has something wrong!")

    return res.text


def get_info_request(leetcode_url: str, leetcode_title: str) -> str:
    try:
        json_data = {"operationName": "questionData", "variables": {"titleSlug": leetcode_title},
                               "query": "query questionData($titleSlug: String!) {  question(titleSlug: $titleSlug) { "
                                        "   questionId    questionFrontendId    boundTopicId    title    titleSlug    "
                                        "content    translatedTitle    translatedContent    isPaidOnly    difficulty  "
                                        "  likes    dislikes    isLiked    similarQuestions    contributors {      "
                                        "username      profileUrl      avatarUrl      __typename    }    "
                                        "langToValidPlayground    topicTags {      name      slug      translatedName "
                                        "     __typename    }    companyTagStats    codeSnippets {      lang      "
                                        "langSlug      code      __typename    }    stats    hints    solution {      "
                                        "id      canSeeDetail      __typename    }    status    sampleTestCase    "
                                        "metaData    judgerAvailable    judgeType    mysqlSchemas    enableRunCode    "
                                        "envInfo    book {      id      bookName      pressName      source      "
                                        "shortDescription      fullDescription      bookImgUrl      pressImgUrl      "
                                        "productUrl      __typename    }    isSubscribed    isDailyQuestion    "
                                        "dailyRecordStatus    editorType    ugcQuestionId    style    __typename  }}"}
        res = requests.post(leetcode_url + "/graphql", json=json_data)
    except Exception:
        raise LeetCodeDailyException("get_info_request has something wrong!")

    return res.text


def leetcode_daily_info_content_request(daily_content: dict, card_id: str) -> dict:
    content = dict()
    content["data"] = dict()
    content["type"] = "template"
    content["data"]["template_id"] = card_id
    content["data"]["template_variable"] = daily_content
    return content


def request_leetcode_daily_from_url(leetcode_url: str, leetcode_card_id: str) -> str:
    # 获取今日每日一题的题名(英文)
    res_title_data = get_title_request(leetcode_url)
    leetcode_title = get_daily_title_from_json(res_title_data)
    # 获取今日每日一题的所有信息
    daily_url = leetcode_url + "/problems/" + leetcode_title
    res_info_data = get_info_request(leetcode_url, leetcode_title)
    try:
        # 转化成json格式
        jsonText = json.loads(res_info_data).get('data').get("question")
        # 题目题号
        no = jsonText.get('questionFrontendId')
        # 题名（中文）
        chinese_leetcode_title = jsonText.get('translatedTitle')
        # 题目难度级别
        level = jsonText.get('difficulty')
        title_string = '(' + no + ') ' + chinese_leetcode_title + ' [' + level + ']'
        # 题目标签
        tags = [element['name'] for element in jsonText.get('topicTags', [])]
        tags_string = ' '.join(tags)
        date_time = datetime.today().date().__str__()

        content = {
            "date": date_time,
            "title": title_string,
            "tags": tags_string,
            "url": daily_url
        }

        reply_leetcode_daily_info = leetcode_daily_info_content_request(content, leetcode_card_id)

    except Exception:
        raise LeetCodeDailyException("request_cve_info_from_url has something wrong!")

    return json.dumps(reply_leetcode_daily_info)