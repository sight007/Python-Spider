import requests
import time
from bs4 import BeautifulSoup
import pymysql
import traceback
import re

headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, ' \
                                               'like Gecko) Chrome/66.0.3359.117 Safari/537.36 '
}

search_url = 'http://kns.cnki.net/kns/request/SearchHandler.ashx?'
base_list_url = 'http://kns.cnki.net/kns/brief/brief.aspx'
list_page = {}

search = {
    'action' : "",
    'NaviCode' : '*',
    'ua' : '1.21',
    'PageName' : 'ASP.brief_result_aspx',
    'DbPrefix' : 'SCDB',
    'DbCatalog' : '中国学术文献网络出版总库',
    'ConfigFile' : 'SCDB.xml',
    'db_opt' : 'CJFQ,CJRF,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',
    'txt_2_sel' : 'TI',
    'txt_2_value1' : '黄连的药理作用与临床应用',
    'txt_2_logical' : 'and',
    'txt_2_relation' : '#CNKI_AND',
    'txt_2_special1' : '=',
    'his' : '0',
    '__' : time.strftime('%a %m %d %Y %H:%M:%S GMT+0800 (CST)')
}

detail = {
    'pagename':'ASP.brief_result_aspx',
    'dbPrefix':'SCDB',
    'dbCatalog':'中国学术文献网络出版总库',
    'ConfigFile':'SCDB.xml',
    'research':'off',
    't':str(int(round(time.time() * 1000))),
    'keyValue':'',
    'S':'1'
}

session = requests.session()


def get_cookies(title):
    search['txt_2_value1'] = title
    r = session.get(search_url, params=search, headers=headers)
    #print(r.url)
    #print(r.status_code)
    return session

def getInfo(title):
    session = get_cookies(title)
    list_page['curpage'] = "1"
    response = session.get(base_list_url, params=detail, headers=headers)
    response.encoding = 'utf-8'
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')

    address = ""
    if soup.select(".fz14") == []:
        address = "没记录"
    else:

        url = "http://kns.cnki.net" + soup.select(".fz14")[0].get("href")
        session.get(url, headers=headers)

        DbCode = re.split('&', url)[5]
        DbName = re.split('&', url)[4]
        FileName = re.split('&', url)[3]
        newUrl = "http://kns.cnki.net/KCMS/detail/detail.aspx?"+DbCode+"&"+DbName+"&"+FileName
        #print(newUrl)

        r = session.get(newUrl,headers=headers)
        r.encoding = 'utf-8'
        #print(r.text)
        soup2 = BeautifulSoup(r.text, 'html.parser')

        for a in soup2.select(".orgn > span > a"):
            address = address + a.string + " "
        updateMySql(title,address)



    '''
        把数据插入到数据库
    '''
def updateMySql(title,address):
    db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "UPDATE zhongyao SET address='%s' WHERE title='%s'" % (address, title)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        # db.rollback()
        # print("error rollback")
    db.close()
    print("---success:"+address)





    '''
    从数据库查找列表
    '''
def getRawList():
    db = pymysql.connect("localhost", "root", "root", "test", use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "select title from zhongyao"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        db.commit()
    except Exception as e:
        traceback.print_exc()
    db.close()

    #print(results)
    return results


def main():
    titles = getRawList()
    for title in titles:
        titleStr = "".join(title)
        print("--start:"+titleStr)
        getInfo(titleStr)
main()