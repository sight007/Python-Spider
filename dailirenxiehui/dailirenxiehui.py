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
    hrefs = soup.select("table.data_f > tbody > tr > td > a.houbian")

    date, tel, fax, companyUrl, email, cAddress = "","","","","",""

    baseUrl = 'http://www.acpaa.cn'
    for i in range(1,len(items)):
        try:
            num = items[i].find_all("td")[1].string
            nick = items[i].find_all("td")[2].string
            name = items[i].find_all("td")[3].string
            type = items[i].find_all("td")[4].string
            principal = items[i].find_all("td")[5].string
            address = items[i].find_all("td")[6].string
            detail = baseUrl + hrefs[i-1].get("href")
            nname,date, tel, fax, companyUrl, email, cAddress = getDetailInfo(detail)
            #print(i, num, nick, name, type, principal, address, detail, date, tel, fax, companyUrl, email, cAddress)
            print(i,name,address)

        except Exception as e:
            print("解析出错name:" + name)
            traceback.print_exc()

        insertMysql(num,nick,name,type,principal,address,detail,nname,date, tel, fax, companyUrl, email, cAddress)



def getDetailInfo(detailUrl):
    detailText = getHTMLText(detailUrl)
    soup = BeautifulSoup(detailText, "html.parser")
    items = soup.select("td > table > tbody")[1].find_all("tr")

    nname,date,tel,fax,companyUrl,email,cAddress = "","","","","","",""

    if items[0].find_all("td")[1].find("b").string != None:
        nname = items[0].find_all("td")[1].find("b").string

    if items[1].find_all("td")[1].string != None:
        date = items[1].find_all("td")[1].string.split("：")[1]

    if items[2].find_all("td")[0].string != None:
        tel = items[2].find_all("td")[0].string.split("：")[1]
    if items[2].find_all("td")[1].string != None:
        fax = items[2].find_all("td")[1].string.split("：")[1]

    companyUrl = items[3].find_all("td")[0].find_all("a")[0].get('href')
    email = items[3].find_all("td")[1].find_all("a")[0].string

    if items[4].find_all("td")[0].string != None:
        cAddress = items[4].find_all("td")[0].string.split("：")[1]
    return nname,date,tel,fax,companyUrl,email,cAddress

def insertMysql(num, nick, name, type, principal, address, detail, nname, date, tel, fax, companyUrl, email, cAddress):
    print("=========================insert ========================")
    db = pymysql.connect("localhost", "root", "root", "agentpantent",use_unicode=True, charset="utf8")
    cursor = db.cursor()
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
    db.close()


def main():
    k = 72
    for n in range(1,1+1):
        url = "http://www.acpaa.cn/view/findAgency.jhtml?pageNumber=" + str(n) + "&agencyId=&shopname=&contact=&area="+str(k)
        print("======第" + str(n) + "页========")
        getList(url)


def mainn():
    url = "http://www.acpaa.cn/view/agencyDetail.jhtml?id=51&pageNumbe=1"
    getDetailInfo(url)


main()

