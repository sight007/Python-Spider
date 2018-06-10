import requests
from bs4 import BeautifulSoup
import traceback
import re
import MySQLdb



def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        #print(r.text)
        return r.text
    except:
         print('getHTMLText error')

def getList(lst,url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")
    a = soup.select("#moderate > ul > li")
    #print(a)

    for li in a:
        infoDict = {}
        infoDict['title'] = li.a['title']
        infoDict['type'] = li.find_all(class_='result_hit')[0].string
        infoDict['desc'] = li.find_all('p')[0].string

        infoDict['class_'] = li.find_all('span')[0].string
        infoDict['legalStatus'] = li.find_all('span')[1].string
        infoDict['docType'] = li.find_all('span')[2].string

        if li.find_all(class_='anhaospan') == []:
            infoDict['docNum'] = ''
        else:
            infoDict['docNum'] = li.find_all(class_='anhaospan')[0].string

        if li.find_all(class_='shijianspan') == []:
            infoDict['date'] = ''
        else:
            infoDict['date'] = li.find_all(class_='shijianspan')[0].string

        if len(li.find_all(class_='shijianspan')) < 2:
            infoDict['money'] = ''
        else:
            infoDict['money'] = li.find_all(class_='shijianspan')[1].string

        #print(infoDict)
        #lst.append(infoDict)
        insertMysql(infoDict['title'],infoDict['type'],infoDict['desc'],infoDict['class_'],infoDict['legalStatus'],infoDict['docType'],infoDict['docNum'],infoDict['date'],infoDict['money'])

def insertMysql(title,type_,desc_,class_,legalStatus,docType,docNum,date_,money):
    db = MySQLdb.connect("localhost", "root", "root", "usertable", charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO zhichanbao \
          (title,type_,desc_,class_,legalStatus,docType,docNum,date_,money) \
           VALUES ('%s', '%s', '%s', '%s', '%s','%s', '%s', '%s', '%s' )" % (title,type_,desc_,class_,legalStatus,docType,docNum,date_,money)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('Inset Error')

    db.close()

def main():
    file = "F:\pythonWork\zhichanbao.txt"
    url = "http://www.iphouse.cn/cases/list.html?casetypeid[]=2&p=2"
    lst = []
    #getList(lst,url)
    for i in range(1,101):
        getList(lst, url)
        print(i)

main()