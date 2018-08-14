import requests
import traceback
import time
import pymysql
import math

"""
鲸准 汽车工业 按照不同的轮次爬取数据
"""



"""
密码登录，主要是得到cookies
"""
def login():
    s = requests.session()
    s.get("https://passport.36kr.com/pages/?ok_url=https%3A%2F%2Frong.36kr.com%2F#/login")

    login_url = "https://passport.36kr.com/passport/sign_in"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Referer": "https://passport.36kr.com/page…https%3A%2F%2Frong.36kr.com%2F",
        "Host": "passport.36kr.com"
    }
    postData = {
        "bind": "false",
        "ktm_reghost": "rong.36kr.com",
        "needCaptcha": "false",
        "ok_url": "https%3A%2F%2Frong.36kr.com%2F",
        "password": "gongzijuan123",
        "type": "login",
        "username": "18771618622"
    }
    login = s.post(login_url,
                   data=postData,
                   headers=dict(referer=login_url),
                   allow_redirects=False
                   )
    identity = s.get("https://rong.36kr.com/api/user/identity")

    return s


"""
获得列表的基础信息
"""
def getList(num):
    s = login()
    asTs, asEncryptedTs = getasEncryptedTs()
    contentUrl = 'https://rong.36kr.com/n/api/search/company?asEncryptedTs='+\
                 asEncryptedTs+'&asTs='+asTs+'&p='+str(num)+\
                 '&kw=%E5%8A%A8%E5%8A%9B%E7%94%B5%E6%B1%A0&sortField=MATCH_RATE'
    first = s.get(contentUrl)

    info = first.json()["data"]["pageData"]["data"]
    #print(info)
    for item in info:
        info = {}
        info["name"] = item["name"]
        info["brief"] = item["brief"]
        info["tags"] = item["tags"]
        info["phase"] = item["phase"]
        info["industryStr"] = item["industryStr"]

        if 'startDate' in item.keys():
            info["startDate"] = time.strftime("%Y-%m", time.localtime(item["startDate"] / 1000.0))
        else:
            info["startDate"] = '--'
        """
        if 
        info["startDate"] = time.strftime("%Y-%m", time.localtime(item["startDate"] / 1000.0))
        """



        info["id"] = item["id"]

        print(info["startDate"])

        info["fullName"], info["intro"], info["address1Desc"], info["address2Desc"] = getDetail(s, info["id"])
        info["memStr"] = getMember(s, info["id"])

        print(info["name"], info["brief"], info["tags"], info["phase"], info["industryStr"], info["startDate"],
              info["id"], info["fullName"], info["intro"], info["address1Desc"], info["address2Desc"], info["memStr"])

        insertMysql(info)


"""
获得url中的加密参数
"""
def getasEncryptedTs():
    asTs = round(time.time()*1000)
    asEncryptedTs = math.cos(asTs / 5 + (abs(3) * (4 * abs(3) / (3 * abs(3) / 3 + 1 - 3 / (8 - 5 / (1 * (1 + 5 * (3 * abs(5 * abs(3) / 3 + 3 / (4 * abs(3) / 3 + 1 - (6 - (10 - 3 * (1 * (5 * abs(3) / 3 + (1 * abs(3) / (8 - 12 / (3 * abs(3 * abs(3) / 3 + 1 - (5 * abs(9 / (9 / (3 * (3 / (3 * abs(3) / 3 + 1 - 3 / (12 / (4 * (1 * abs(3) / 3 + 3 / (3 * (3 * abs(3) / 3 + (1 * abs(3) / 3 + 1 - (3 / (4 * abs(9 / (5 * abs(3) / 3 + 1 - 1 + 3 - 5)) / 3 + 1 - 1) * 4 / 3 * 1 + 5 - 5)) - 1) / 4 * 4 / 3 * 1 + 5 - 5) - 1) + 5 - 5) * 4 / 3) * 4 / 3) * 4 + 5 - 5) / 4 * 4 / 3 * 3 / 4 * 4 / 3 * 1 + 5 - 5) * 4 / 3 * 3 / 4 * 4 / 3)) / 3 + 1 - 1 + 1 - 5)) / 3 + 1 - 1) * 3.75 / 3 / 1) + 1 - 1) - 1) + 5 - 5) / 4 * 4 / 3 / 1) / 1)) * 4 / 3 - 1 + 3 - 5) / 3 + 1 - 1) / 4 * 4 / 3 - 5) + 5 - 5))) + 1 - 1) / 3 + 1 - 1))
    #print(asTs,asEncryptedTs)
    return str(asTs),str(asEncryptedTs)



"""
根据公司的ID得到详细信息
"""
def getDetail(session, num_id):
    asTs, asEncryptedTs = getasEncryptedTs()
    detailUrl = "https://rong.36kr.com/n/api/company/"+str(num_id)+'?asEncryptedTs='+asEncryptedTs+'&asTs='+asTs

    r = session.get(detailUrl)
    allDetail = r.json()["data"]
    print(detailUrl)

    fullName = allDetail["fullName"]

    intro = ''
    if 'intro' in allDetail.keys():
        info = allDetail["intro"]
    else:
        intro = '--'

    address1Desc = ''
    if 'address1Desc' in allDetail.keys():
        address1Desc = allDetail["address1Desc"]
    else:
        address1Desc = '--'

    address2Desc = ''
    if 'address2Desc' in allDetail.keys():
        address2Desc = allDetail["address2Desc"]
    else:
        address2Desc = '--'


    return fullName, intro, address1Desc, address2Desc


"""
根据公司的id得到创始人信息
"""
def getMember(session, id):
    memberlUrl = "https://rong.36kr.com/n/api/company/" + str(id) + "/member"
    r = session.get(memberlUrl)
    members = r.json()["data"]["members"]

    memStr = ""
    for member in members:
        memStr = memStr + member["name"] + " "

    print(memStr)
    return memStr


"""
连接数据库，插入到数据库
"""


def insertMysql(info):
    print("---- insert ----")
    db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO donglidianchi" \
          "(" \
          "name,brief,tags,phase,industryStr,startDate,companyId,fullName,intro,address1Desc,address2Desc,memStr" \
          ") \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (info["name"], info["brief"], info["tags"], info["phase"], info["industryStr"], info["startDate"],
           info["id"], info["fullName"], info["intro"], info["address1Desc"], info["address2Desc"], info["memStr"])
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        # db.rollback()
        # print("error rollback")
    db.close()


'''
#START-----------------------------------------new DB connection function TEST---------------------------------------------
def openDB():
    db = pymysql.connect("localhost", "root", "root", "agentpantent",use_unicode=True, charset="utf8")
    cursor = db.cursor()
    return db,cursor
name
def closeDB(db):
    db.close()

def SQL(db,cursor):
    sql = "INSERT INTO company" \
          "(" \
          "num, nick, name, type, principal, address, detail, nname, date, tel, fax, companyUrl, email, cAddress" \
          ") \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
           (num, nick, name, type, principal, address, detail, nname, date, tel, fax, companyUrl, email, cAddress)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        #db.rollback()
        #print("error rollback")
#END-----------------------------------------new DB connection function TEST---------------------------------------------
'''


def main():
    for num in range(1, 11+1):
        getList(num)
        time.sleep(1)
main()

