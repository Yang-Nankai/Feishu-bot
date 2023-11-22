# -*- coding: utf-8 -*-
# @Time    : 2023/11/21 22:31
# @Comment :


import httpx
import requests
import datetime
import json

requests.packages.urllib3.disable_warnings()

vul_like = ['weblogic', 'apache']  # 关注的组件，可添加
risk_like = ['CRITICAL', 'HIGH']  # 关注的威胁级别，可添加
care = 1  # 0表示只接收关注组件的漏洞，1表示所有组件的高危漏洞

# 这里得换接口才行
url = 'https://services.nvd.nist.gov/rest/json/cves/2.0'

def get_cve():
    # 时间比我们晚，#取三天前的漏洞才有cvss评分
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)  # 3
    pub_start_date = str(yesterday) + 'T00:00:00.000%2B01:00'
    pub_end_date = str(today) + 'T00:00:00.000%2B01:00'
    cve_content = []  # save the request cve info

    request_url = url + '?lastModStartDate={}&lastModEndDate={}'.format(pub_start_date, pub_end_date)

    response = requests.get(request_url, verify=False, timeout=20)
    res = json.loads(response.text)
    if res['totalResults'] > 0:
        cve_content.extend(res_content(res))


# 增加数据库使数据入库
# 增加定时任务/或者依靠飞书捷径来实现

def res_content(res) -> list:
    content = []

    for i in range(res['totalResults']):
        id = res['vulnerabilities'][i]['cve']['id']
        pubdate = res['vulnerabilities'][i]['cve']['published']
        try:
            base_severity = res['vulnerabilities'][i]['cve']['metrics']['cvssMetricV31'][0]['cvssData']['base_severity']
            base_score = str(res['vulnerabilities'][i]['cve']['metrics']['cvssMetricV31'][0]['cvssData']['base_score'])
            base_severity_score = base_severity + " " + base_score
            vuln_status = res['vulnerabilities'][i]['cve']['vuln_status']
            cve_source = res['vulnerabilities'][i]['cve']['references'][0]['url']
            description = res['vulnerabilities'][i]['cve']['descriptions'][0]['value']
            cve_single = {
                "cve_number": id,
                "cve_time": pubdate,
                "cve_rank": base_severity_score,
                "cve_description": description,
                "cve_status": vuln_status,
                "cve_source": cve_source
            }
            if base_severity in risk_like:
                content.append(cve_single)
        except Exception as e:
            print(e)

    return content



def main():
    get_cve()


if __name__ == "__main__":
    main()
