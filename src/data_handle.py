# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 16:45
# @Comment :


# -*- coding: utf-8 -*-
# @Time    : 2023/11/22 16:18
# @Comment :

import sqlite3
import os


# initialize database
def create_database():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../', 'data', 'cve_data.db'))
    print("[]create_database function connect database success!")
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS cve_info_list
                   (cve_number varchar(255) PRIMARY KEY,
                    cve_time varchar(255),
                    cve_rank varchar(255),
                    cve_status varchar(255),
                    cve_description varchar(2000),
                    cve_source varchar(255));''')
        print("Successfully build CVE info table.")
    except Exception as e:
        print("Unsuccessfully Build the monitor table! ERROr: {}".format(e))
    conn.commit()  # 数据库存储在硬盘上需要commit  存储在内存中的数据库不需要
    conn.close()


# insert the cve info into the sqlite3
def cve_insert_into_sqlite3(data: list):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '../', 'data', 'cve_data.db'))
    print("cve_insert_into_sqlite3 function open database successfully!")
    cur = conn.cursor()
    for i in range(len(data)):
        try:
            cve_number = data[i]['cve_number'].upper()
            cve_time = data[i]['cve_time']
            cve_rank = data[i]['cve_rank']
            cve_status = data[i]['cve_status']
            cve_description = data[i]['cve_description'].strip().replace("\'", "")
            cve_source = data[i]['cve_source']
            cur.execute("INSERT OR IGNORE INTO cve_info_list (cve_number,cve_time,cve_rank,cve_status,cve_description,"
                        "cve_source) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(cve_number, cve_time,
                                                                                         cve_rank, cve_status,
                                                                                         cve_description,
                                                                                         cve_source))
            print("{} insert data successfully!".format(cve_number))
        except Exception as e:
            print("Unsuccessfully insert data! ERROR: {}".format(e))
            pass
    conn.commit()
    conn.close()
