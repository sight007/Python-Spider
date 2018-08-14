import requests
from bs4 import BeautifulSoup
import traceback
#import re
import pymysql

'''
获取页面源代码
'''
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


def getListUrl(url):
    listUrlText = getHTMLText(url)
    soup = BeautifulSoup(listUrlText, "html.parser")
    urlItems = soup.select("#myul > li")
    #print(len(urlItems))
    for urlItem in urlItems:

        title=urlItem.find('a').string
        print(title)

        rhref = urlItem.find('a').get('href')
        href = rhref.replace('./', 'http://www.csrc.gov.cn/pub/newsite/ssgsjgb/bgczfkyj/')
        #print('-----'+href)
        print(href)

        public_date=urlItem.find('span').string
        print(public_date)

        content = getList(href)
        insertMysql(title, href, public_date, content)


def getList(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")

    if len(soup.select(".Custom_UnionStyle")) == 0:
        content=soup.select(".content")[0].text
    else:
        #print(soup.select(".Custom_UnionStyle"))
        content=soup.select(".Custom_UnionStyle")[0].text
    print(content[:100])

    return content


def insertMysql(title,href,public_date,content):
    print("=========================insert ========================")
    db = pymysql.connect("localhost", "root", "root", "agentpantent",use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "INSERT INTO zhengjianhui3" \
          "(" \
          "title,url,public_date,content" \
          ") \
           VALUES ('%s', '%s', '%s', '%s')" % \
           (title,href,public_date,content)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        traceback.print_exc()
        db.rollback()
        print("error rollback")
    db.close()

def main():

    for i in range(0,25+1):
        print("第"+str(i)+"页")
        if i==0:
            url='http://www.csrc.gov.cn/pub/newsite/ssgsjgb/bgczfkyj/index.htm'
        else:
            url='http://www.csrc.gov.cn/pub/newsite/ssgsjgb/bgczfkyj/index_'+str(i)+'.htm'

        getListUrl(url)
main()