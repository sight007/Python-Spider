# -*- coding:utf-8 -*-

import requests
import time
import json

from bs4 import BeautifulSoup

url = "http://202.127.48.148/searchUser/searchAction!getVRecordListPage.do"

t = time.time()
nowTime = int(round(t * 1000))

param = {"_search":"false",\
            "nd":nowTime,\
            "rows":"100",\
            "page":"33",\
            "sidx":"RECORD_NUM",\
            "sord":"desc",\
            "APPLY_USER_NAME":"",\
            "RECORD_NAME":"",\
            "RECORD_NUM":"",\
            "REGISTER_NUM":"",\
            "PRODUCT_TYPE":"",\
            "VERIFY_STATE":"",\
            "LEGALOF_USER_NAME":"",\
            "RECORD_STATE":"",\
            "CHECK_MERCH":"",\
            "CAN_USE_PRODUCT":"",\
            "COUNTRY":"",\
            "REGISTER_TYPE":"10",\
            "ISLIKE":"true",\
            "RECORD_TYPE":""}

try:
    r = requests.post(url, data=param, timeout=60)
    print r.status_code
    r.encoding = r.apparent_encoding
    a = json.loads(r.text,encoding="utf-8")
    #print a
    #print type(a)
    #b = json.dumps(a,ensure_ascii=False)
    #print type(b)

    #print a['rows']
    b = json.dumps(a['rows'],ensure_ascii=False)
    print b
    print type(b)
    fh = open("4.txt", 'w')
    fh.write(b.encode('utf8'))
    print "write____Success"
    fh.close()

    print "-------Success--------"
except:
    print "_____________get Json error++++++++++++++"

