# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 16:18
# @Comment :

import sqlite3
import os


# 初始化数据库
def create_database():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../', 'data', 'cve_data.db'))
    print("[]create_database 函数 连接数据库成功！")
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS cve_info_list
                   (cve_number varchar(255),
                    cve_time varchar(255),
                    cve_rank varchar(255),
                    cve_status varchar(255),
                    cve_description varchar(2000),
                    cve_source varchar(255));''')
        print("成功创建CVE信息表")
    except Exception as e:
        print("创建监控表失败！报错：{}".format(e))
    conn.commit()  # 数据库存储在硬盘上需要commit  存储在内存中的数据库不需要
    conn.close()


def cve_insert_into_sqlite3(data: list):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../', 'data', 'cve_data.db'))
    print("cve_insert_into_sqlite3 函数 打开数据库成功！")
    cur = conn.cursor()
    for i in range(len(data)):
        try:
            cve_number = data[i]['cve_number'].upper()
            cve_time = data[i]['cve_time']
            cve_rank = data[i]['cve_rank']
            cve_status = data[i]['cve_status']
            cve_description = data[i]['cve_description'].strip().replace("\'", "")
            cve_source = data[i]['cve_source']
            cur.execute("INSERT INTO cve_info_list (cve_number,cve_time,cve_rank,cve_status,cve_description,"
                        "cve_source) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(cve_number, cve_time,
                                                                                               cve_rank, cve_status,
                                                                                               cve_description,
                                                                                               cve_source))
            print("cve_insert_into_sqlite3 函数: {}插入数据成功！".format(cve_number))
        except Exception as e:
            print("插入数据失败！报错：{}".format(e))
            pass
    conn.commit()
    conn.close()


data_list = [{'cve_number': 'CVE-2023-3961', 'cve_time': '2023-11-03T13:15:08.723', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'A path traversal vulnerability was identified in Samba when processing client pipe names connecting to Unix domain sockets within a private directory. Samba typically uses this mechanism to connect SMB clients to remote procedure call (RPC) services like SAMR LSA or SPOOLSS, which Samba initiates on demand. However, due to inadequate sanitization of incoming client pipe names, allowing a client to send a pipe name containing Unix directory traversal characters (../). This could result in SMB clients connecting as root to Unix domain sockets outside the private directory. If an attacker or client managed to send a pipe name resolving to an external service using an existing Unix domain socket, it could potentially lead to unauthorized access to the service and consequential adverse events, including compromise or service crashes.',
              'cve_status': 'Modified', 'cve_source': 'https://access.redhat.com/errata/RHSA-2023:6209'},
             {'cve_number': 'CVE-2023-36018', 'cve_time': '2023-11-14T18:15:31.413', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'Visual Studio Code Jupyter Extension Spoofing Vulnerability',
              'cve_status': 'Analyzed',
              'cve_source': 'https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-36018'},
             {'cve_number': 'CVE-2023-20596', 'cve_time': '2023-11-14T19:15:16.083', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'Improper input validation in the SMM Supervisor may allow an attacker with a compromised SMI handler to gain Ring0 access potentially leading to arbitrary code execution.',
              'cve_status': 'Analyzed',
              'cve_source': 'https://www.amd.com/en/corporate/product-security/bulletin/AMD-SB-7011'},
             {'cve_number': 'CVE-2023-34060', 'cve_time': '2023-11-14T21:15:09.253', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'VMware Cloud Director Appliance contains an authentication bypass vulnerability in case VMware Cloud Director Appliance was upgraded to 10.5 from\nan older version.\xa0On an upgraded version of VMware Cloud Director Appliance 10.5, a malicious actor with network access to the appliance can bypass login\nrestrictions when authenticating on port 22 (ssh) or port 5480 (appliance management console) . This bypass is not present on port 443 (VCD provider\nand tenant login). On a new installation of VMware Cloud Director Appliance 10.5, the bypass is not present.\xa0VMware Cloud Director Appliance is impacted since it uses an affected version of sssd from the underlying Photon OS. The sssd issue is no longer present in versions of Photon OS that ship with sssd-2.8.1-11 or higher (Photon OS 3) or sssd-2.8.2-9 or higher (Photon OS 4 and 5).',
              'cve_status': 'Analyzed', 'cve_source': 'https://github.com/vmware/photon/wiki/Security-Update-3.0-687'},
             {'cve_number': 'CVE-2023-36049', 'cve_time': '2023-11-14T21:15:10.083', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': '.NET, .NET Framework, and Visual Studio Elevation of Privilege Vulnerability',
              'cve_status': 'Analyzed',
              'cve_source': 'https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-36049'},
             {'cve_number': 'CVE-2023-45614', 'cve_time': '2023-11-14T23:15:09.313', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': "There are buffer overflow vulnerabilities in the underlying CLI service that could lead to unauthenticated remote code execution by sending specially crafted packets destined to the PAPI (Aruba's access point management protocol) UDP port (8211). Successful exploitation of these vulnerabilities result in the ability to execute arbitrary code as a privileged user on the underlying operating system.",
              'cve_status': 'Analyzed',
              'cve_source': 'https://www.arubanetworks.com/assets/alert/ARUBA-PSA-2023-017.txt'},
             {'cve_number': 'CVE-2023-45615', 'cve_time': '2023-11-14T23:15:09.487', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': "There are buffer overflow vulnerabilities in the underlying CLI service that could lead to unauthenticated remote code execution by sending specially crafted packets destined to the PAPI (Aruba's access point management protocol) UDP port (8211). Successful exploitation of these vulnerabilities result in the ability to execute arbitrary code as a privileged user on the underlying operating system.",
              'cve_status': 'Analyzed',
              'cve_source': 'https://www.arubanetworks.com/assets/alert/ARUBA-PSA-2023-017.txt'},
             {'cve_number': 'CVE-2023-45616', 'cve_time': '2023-11-14T23:15:09.663', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': "There is a buffer overflow vulnerability in the underlying AirWave client service that could lead to unauthenticated remote code execution by sending specially crafted packets destined to the PAPI (Aruba's access point management protocol) UDP port (8211). Successful exploitation of this vulnerability results in the ability to execute arbitrary code as a privileged user on the underlying operating system.",
              'cve_status': 'Analyzed',
              'cve_source': 'https://www.arubanetworks.com/assets/alert/ARUBA-PSA-2023-017.txt'},
             {'cve_number': 'CVE-2023-43979', 'cve_time': '2023-11-15T01:15:07.760', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'ETS Soft ybc_blog before v4.4.0 was discovered to contain a SQL injection vulnerability via the component Ybc_blogBlogModuleFrontController::getPosts().',
              'cve_status': 'Analyzed',
              'cve_source': 'https://security.friendsofpresta.org/modules/2023/11/14/ybc_blog.html'},
             {'cve_number': 'CVE-2023-47308', 'cve_time': '2023-11-15T01:15:07.810', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'In the module "Newsletter Popup PRO with Voucher/Coupon code" (newsletterpop) before version 2.6.1 from Active Design for PrestaShop, a guest can perform SQL injection in affected versions. The method `NewsletterpopsendVerificationModuleFrontController::checkEmailSubscription()` has sensitive SQL calls that can be executed with a trivial http call and exploited to forge a SQL injection.',
              'cve_status': 'Analyzed',
              'cve_source': 'https://github.com/friends-of-presta/security-advisories/blob/main/_posts/2023-11-09-newsletterpop.md'},
             {'cve_number': 'CVE-2023-47678', 'cve_time': '2023-11-15T02:15:06.800', 'cve_rank': 'CRITICAL 9.1',
              'cve_description': 'An improper access control vulnerability exists in RT-AC87U all versions. An attacker may read or write files that are not intended to be accessed by connecting to a target device via tftp.',
              'cve_status': 'Analyzed', 'cve_source': 'https://jvn.jp/en/vu/JVNVU96079387/'},
             {'cve_number': 'CVE-2021-35437', 'cve_time': '2023-11-16T05:15:24.303', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'SQL injection vulnerability in LMXCMS v.1.4 allows attacker to execute arbitrary code via the TagsAction.class.',
              'cve_status': 'Analyzed',
              'cve_source': 'https://github.com/GHA193/Vulns/blob/main/lmxcms%20injection.md'},
             {'cve_number': 'CVE-2023-47003', 'cve_time': '2023-11-16T05:15:29.927', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'An issue in RedisGraph v.2.12.10 allows an attacker to execute arbitrary code and cause a denial of service via a crafted string in DataBlock_ItemIsDeleted.',
              'cve_status': 'Analyzed', 'cve_source': 'https://github.com/RedisGraph/RedisGraph/issues/3063'},
             {'cve_number': 'CVE-2023-40151', 'cve_time': '2023-11-21T00:15:06.953', 'cve_rank': 'CRITICAL 10.0',
              'cve_description': 'When user authentication is not enabled the shell can execute commands with the highest privileges. Red Lion SixTRAK and VersaTRAK Series RTUs with authenticated users enabled (UDR-A) any Sixnet UDR message will meet an authentication challenge over UDP/IP. When the same message comes over TCP/IP the RTU will simply accept the message with no authentication challenge.',
              'cve_status': 'Awaiting Analysis',
              'cve_source': 'https://support.redlion.net/hc/en-us/articles/19339209248269-RLCSIM-2023-05-Authentication-Bypass-and-Remote-Code-Execution'},
             {'cve_number': 'CVE-2023-6144', 'cve_time': '2023-11-21T00:15:07.353', 'cve_rank': 'CRITICAL 9.1',
              'cve_description': 'Dev blog v1.0 allows to exploit an account takeover through the "user" cookie. With this, an attacker can access any user\'s session just by knowing their username.',
              'cve_status': 'Awaiting Analysis', 'cve_source': 'https://fluidattacks.com/advisories/almighty/'},
             {'cve_number': 'CVE-2023-42770', 'cve_time': '2023-11-21T01:15:07.100', 'cve_rank': 'CRITICAL 10.0',
              'cve_description': 'Red Lion SixTRAK and VersaTRAK Series RTUs with authenticated users enabled (UDR-A) any Sixnet UDR message will meet an authentication challenge over UDP/IP. When the same message is received over TCP/IP the RTU will simply accept the message with no authentication challenge.',
              'cve_status': 'Awaiting Analysis',
              'cve_source': 'https://https://support.redlion.net/hc/en-us/articles/19339209248269-RLCSIM-2023-05-Authentication-Bypass-and-Remote-Code-Execution'},
             {'cve_number': 'CVE-2023-4149', 'cve_time': '2023-11-21T07:15:10.093', 'cve_rank': 'CRITICAL 9.8',
              'cve_description': 'A vulnerability in the web-based management allows an unauthenticated remote attacker to inject arbitrary system commands and gain full system control. Those commands are executed with root privileges. The vulnerability is located in the user request handling of the web-based management.',
              'cve_status': 'Awaiting Analysis', 'cve_source': 'https://cert.vde.com/en/advisories/VDE-2023-037'}]
create_database()
cve_insert_into_sqlite3(data_list)
