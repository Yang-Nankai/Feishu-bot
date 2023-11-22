# -*- coding: utf-8 -*-
# @Time    : 2023/11/21 22:15
# @Comment :

import re
import datetime
import requests
from collections import OrderedDict


GITHUB_TOKEN = ""
black_user = []
counter = {}

github_headers = {
    'Authorization': "token {}".format(GITHUB_TOKEN)
}


# 根据排序获取本年前20条CVE
def getNews():
    today_cve_info_tmp = []
    try:
        # 抓取本年的
        year = datetime.datetime.now().year
        api = "https://api.github.com/search/repositories?q=CVE-{}&sort=updated".format(year)
        json_str = requests.get(api, headers=github_headers, timeout=10).json()
        # cve_total_count = json_str['total_count']
        # cve_description = json_str['items'][0]['description']
        today_date = datetime.date.today()
        n = len(json_str['items'])
        if n > 30:
            n = 30
        for i in range(0, n):
            cve_url = json_str['items'][i]['html_url']
            if cve_url.split("/")[-2] not in black_user:
                try:
                    cve_name_tmp = json_str['items'][i]['name'].upper()
                    cve_name = re.findall('(CVE\-\d+\-\d+)', cve_name_tmp)[0].upper()
                    pushed_at_tmp = json_str['items'][i]['created_at']
                    pushed_at = re.findall('\d{4}-\d{2}-\d{2}', pushed_at_tmp)[0]
                    if pushed_at == str(today_date):
                        today_cve_info_tmp.append({"cve_name": cve_name, "cve_url": cve_url, "pushed_at": pushed_at})
                    else:
                        print("[-] 该{}的更新时间为{}, 不属于今天的CVE".format(cve_name, pushed_at))
                except Exception as e:
                    pass
            else:
                pass
        today_cve_info = OrderedDict()
        for item in today_cve_info_tmp:
            user_name = item['cve_url'].split("/")[-2]
            if user_name in counter:
                if counter[user_name] < 3:
                    counter[user_name] +=1
                    today_cve_info.setdefault(item['cve_name'], {**item, })
            else:
                counter[user_name] = 0
                today_cve_info.setdefault(item['cve_name'], {**item, })
        today_cve_info = list(today_cve_info.values())

        return today_cve_info
        # return cve_total_count, cve_description, cve_url, cve_name
        #\d{4}-\d{2}-\d{2}

    except Exception as e:
        print(e, "github链接不通")
        return '', '', ''


today_cve_info = getNews()
print(today_cve_info)