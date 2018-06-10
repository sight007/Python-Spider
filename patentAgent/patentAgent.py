import requests
from bs4 import BeautifulSoup
import traceback
#import re
import pymysql



def getHTMLText(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        #print(r.text)
        return r.text
    except Exception as e:
        print('getHTMLText异常,url:'+url)
        traceback.print_exc()

def getList(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")
    items = soup.select(".data_f > tbody > tr")

    name, num, code, company, type = "","","","",""

    for i in range(1,len(items)):
        try:
            name = items[i].find_all('td')[1].string
            num = items[i].find_all('td')[2].string
            code = items[i].find_all('td')[3].string
            company = items[i].find_all('td')[4].string
            type = items[i].find_all('td')[5].string
        except Exception as e:
            traceback.print_exc()
            continue
        print(str(i)+"  "+name)
        insertMysql(name, num, code, company, type)

def insertMysql(name, num, code, company, type):
    print("=========================insert ========================")
    db = pymysql.connect("localhost", "root", "root", "agentpantent",use_unicode=True, charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO agentpeople" \
          "(" \
          "name, num, code, company, type" \
          ") \
           VALUES ('%s', '%s', '%s', '%s', '%s')" % \
           (name, num, code, company, type)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        db.rollback()
        print("error rollback")
    db.close()

def main():

    for i in range(1,117+1):
        print("第"+str(i)+"页")
        url = "http://www.acpaa.cn/font/agentBatch/list.jhtml?pageNumber=" + str(i) + "&agencyID=&company=&batch=&username=&practice="
        getList(url)

main()