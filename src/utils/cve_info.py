# -*- coding: utf-8 -*-
# @Time    : 2023/11/21 22:31
# @Comment :


import datetime
import json
import requests
from src.utils.Exceptions import CVEDataException
from src.data_handle import cve_insert_into_sqlite3

requests.packages.urllib3.disable_warnings()

vul_like = ['weblogic', 'apache']  # 关注的组件，可添加
risk_like = ['CRITICAL']  # 关注的威胁级别，可添加
care = 1  # 0表示只接收关注组件的漏洞，1表示所有组件的高危漏洞


def cve_info_content_request(cve_content: dict, card_id: str) -> dict:
    content = dict()
    content["data"] = dict()
    content["type"] = "template"
    content["data"]["template_id"] = card_id
    content["data"]["template_variable"] = cve_content
    return content


def request_cve_info_from_url(cve_url: str, cve_card_id: str) -> str:
    # 时间比我们晚，#取三天前的漏洞才有cvss评分
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)  # 3
    pub_start_date = str(yesterday) + 'T00:00:00.000%2B01:00'
    pub_end_date = str(today) + 'T00:00:00.000%2B01:00'
    cve_content = []  # save the request cve info

    request_url = cve_url + '?lastModStartDate={}&lastModEndDate={}'.format(pub_start_date, pub_end_date)
    response = requests.get(request_url, verify=False, timeout=60)
    res = json.loads(response.text)

    if res['totalResults'] > 0:
        cve_content = res_content(res)

    if len(cve_content) > 0:
        content = {
            "start_time": pub_start_date,
            "end_time": pub_end_date,
            "cve_set": cve_content
        }
        reply_cve_info = cve_info_content_request(content, cve_card_id)
    else:
        raise CVEDataException("No CVE Info Data.")

    return json.dumps(reply_cve_info)


def get_the_metrics_data(metrics: dict):
    if 'cvssMetricV31' in metrics:
        return str(metrics['cvssMetricV31'][0]['cvssData']['baseSeverity']), str(
            metrics['cvssMetricV31'][0]['cvssData']['baseScore'])
    elif 'cvssMetricV2' in metrics:
        return str(metrics['cvssMetricV2'][0]['baseSeverity']), str(metrics['cvssMetricV2'][0]['cvssData']['baseScore'])
    else:
        return "", ""


def get_the_source_data(references: list) -> str:
    if len(references) == 0:
        return ""
    else:
        return references[0]['url']


def res_content(res) -> list:
    content = []
    for i in range(res['totalResults']):
        cve_id = res['vulnerabilities'][i]['cve']['id']
        pubdate = res['vulnerabilities'][i]['cve']['published']
        try:
            base_severity, base_score = get_the_metrics_data(res['vulnerabilities'][i]['cve']['metrics'])
            base_severity_score = base_severity + " " + base_score
            vuln_status = res['vulnerabilities'][i]['cve']['vulnStatus']
            cve_source = get_the_source_data(res['vulnerabilities'][i]['cve']['references'])
            description = res['vulnerabilities'][i]['cve']['descriptions'][0]['value'].strip()
            cve_single = {
                "cve_number": cve_id,
                "cve_time": pubdate,
                "cve_rank": base_severity_score,
                "cve_description": description,
                "cve_status": vuln_status,
                "cve_source": cve_source
            }
            if base_severity in risk_like:
                content.append(cve_single)
        except Exception:
            raise CVEDataException("Append Exception!")

    # insert cve info to sqlite3
    cve_insert_into_sqlite3(content)

    return content
