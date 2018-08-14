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

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "Referer": "https://passport.36kr.com/page…https%3A%2F%2Frong.36kr.com%2F",
        "Host": "passport.36kr.com"
    }


def login():
    s = requests.session()
    s.get("https://passport.36kr.com/pages/?ok_url=https%3A%2F%2Frong.36kr.com%2F#/login")

    login_url = "https://passport.36kr.com/passport/sign_in"

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
    #print(identity.status_code)

    return s


"""
获得列表的基础信息
"""
def getList(phase, num):
    s = login()
    contentUrl = "https://rong.36kr.com/n/api/column/0/company?phase=" \
                 + phase + \
                 "&industry=AUTO&sortField=HOT_SCORE&p=" + str(num)
    first = s.get(contentUrl)

    info = first.json()["data"]["pageData"]["data"]
    for item in info:
        info = {}
        info["name"] = item["name"]
        if ("cityStr" in item.keys()):
            info["cityStr"] = item["cityStr"]
        else:
            info["cityStr"] = ""
        if ("brief" in item.keys()):
            info["brief"] = item["brief"]
        else:
            info["brief"] = ""
        info["tags"] = " ".join(item["tags"])
        info["phase"] = item["phase"]
        info["industryStr"] = item["industryStr"]
        if("startDate" in item.keys()):
            info["startDate"] = time.strftime("%Y-%m", time.localtime(item["startDate"] / 1000.0))
        else:
            info["startDate"] = ""
        info["id"] = item["id"]
        print(info["name"],info["cityStr"], info["brief"], info["tags"], info["phase"], info["industryStr"], info["startDate"],
              info["id"])

        #info["fullName"], info["intro"], info["address1Desc"], info["address2Desc"] = getDetail(s, id)
        #info["memStr"] = getMember(s, id)

        """
        print(info["name"], info["brief"], info["tags"], info["phase"], info["industryStr"], info["startDate"],
              info["id"], info["fullName"], info["intro"], info["address1Desc"], info["address2Desc"], info["memStr"])
        """
        insertMysql(info)


"""
连接数据库，插入到数据库
"""
def insertMysql(info):
    print("---- insert ----")
    db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO car_industry" \
          "(" \
          "name,city,brief,tags,phase,industryStr,startDate,companyId" \
          ") \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (info["name"],info["cityStr"], info["brief"], info["tags"], info["phase"], info["industryStr"], info["startDate"],
           str(info["id"]))
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        # db.rollback()
        # print("error rollback")
    db.close()



#-----------START------后续的更新（获得基本数据之后）-------------------------------------------------

def detailInfo():
    s = login()
    idList = getCompanyId()
    for id in idList:
        fullName, intro, address1Desc, address2Desc = getDetail(s,id)
        memStr = getMember(s,id)
        print(fullName, intro, address1Desc, address2Desc,memStr)
        update(fullName, intro, address1Desc, address2Desc, memStr, id)
        #time.sleep(1)

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
def getDetail(session, id):
    asTs, asEncryptedTs = getasEncryptedTs()
    detailUrl = "https://rong.36kr.com/n/api/company/" + str(id)\
                +"?asEncryptedTs="+asEncryptedTs+"&asTs="+asTs
    r = session.get(detailUrl)
    #print(r.status_code)
    allDetail = r.json()["data"]
    #print(type(allDetail))

    fullName, intro, address1Desc, address2Desc = "", "", "", ""
    if ("fullName" in allDetail.keys()):
        fullName = allDetail["fullName"]
    if ("intro" in allDetail.keys()):
        intro = allDetail["intro"]
    if ("address1Desc" in allDetail.keys()):
        address1Desc = allDetail["address1Desc"]
    if("address2Desc" in allDetail.keys()):
        address2Desc = allDetail["address2Desc"]

    return fullName, intro, address1Desc, address2Desc


"""
根据公司的id得到创始人信息
"""
def getMember(session, id):
    asTs, asEncryptedTs = getasEncryptedTs()
    memberlUrl = "https://rong.36kr.com/n/api/company/" + str(id) + "/member"\
                 +"?asEncryptedTs="+asEncryptedTs+"&asTs="+asTs
    r = session.get(memberlUrl)
    #print(r.json())

    memStr = ""
    if("members" not in r.json()["data"].keys()):
        print("没有创始人信息")
    else:
        members = r.json()["data"]["members"]
        for member in members:
            memStr = memStr + member["name"] + " "

    #print(memStr)
    return memStr


"""
从数据库里面获得公司id的列表
"""
def getCompanyId():
    db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "select companyId from car_industry WHERE intro=''"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except Exception as e:
        traceback.print_exc()
        # db.rollback()
        # print("error rollback")
    db.close()
    #print(type(results))
    idList = []
    for item in results:
        idList.append("".join(item))

    return idList


"""
把detai信息更新进入数据库
"""
def update(fullName, intro, address1Desc, address2Desc, memStr, companyId):
    db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "update car_industry set " \
          "fullName='%s',intro='%s',address1Desc='%s',address2Desc='%s',memStr='%s' " \
          "where companyId='%s'" % (fullName, intro, address1Desc, address2Desc, memStr, companyId)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        db.rollback()
        print("error rollback")
    db.close()

#-----------END------后续的更新（获得基本数据之后）-------------------------------------------------


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
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
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
    """
    phase = ['SEED', 'ANGEL', 'PRE_A', 'A', 'A_PLUS', 'PRE_B', 'B', 'B_PLUS', 'C', 'C_PLUS', 'D', 'E']
    total = 24
    total = math.ceil(total / 20)
    print(total)
    for num in range(1, total + 1):
        print("第"+str(num)+"轮开始")
        #getList("E", num)   #获取基本信息
    """
    #getCompanyId()
    #update("aa","aa","aa","aa","aa","39025")
    #getasEncryptedTs()
    detailInfo()


main()
