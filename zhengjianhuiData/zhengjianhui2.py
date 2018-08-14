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
        href = rhref.replace('../../../..', 'http://www.csrc.gov.cn/pub')

        print(href)

        public_date=urlItem.find('span').string
        print(public_date)

        index_num, classify, agent, doc_date, name, doc_num, keyword, content = getList(href)
        insertMysql(title, href, public_date, index_num, classify, agent, doc_date, name, doc_num, keyword, content)


def getList(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html,"html.parser")
    items = soup.select("#headContainer > tbody > tr")

    index_num = items[0].find_all('td')[1].text
    print(index_num)

    classify=items[0].find_all('td')[2].text
    print(classify)

    agent=items[1].find_all('td')[1].text
    print(agent)

    doc_date=items[1].find_all('td')[2].text
    print(doc_date)

    name=items[2].find_all('span')[0].text
    print(name)

    doc_num=items[3].find_all('td')[1].text
    print(doc_num)

    keyword=items[3].find_all('td')[2].text
    print(keyword)

    content=soup.select(".content")[0].text
    print(content)

    return index_num,classify,agent,doc_date,name,doc_num,keyword,content


def insertMysql(title,href,public_date,index_num,classify,agent,doc_date,name,doc_num,keyword,content):
    print("=========================insert ========================")
    db = pymysql.connect("localhost", "root", "root", "agentpantent",use_unicode=True, charset="utf8")
    cursor = db.cursor()

    sql = "INSERT INTO zhengjianhui2" \
          "(" \
          "title,url,public_date,index_num,classify,agent,doc_date,name,doc_num,keyword,content" \
          ") \
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
           (title,href,public_date,index_num,classify,agent,doc_date,name,doc_num,keyword,content)
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
            url='http://www.csrc.gov.cn/pub/newsite/ssgsjgb/ssbbgczxzxkhz/jggs/index.htm'
        else:
            url='http://www.csrc.gov.cn/pub/newsite/ssgsjgb/ssbbgczxzxkhz/jggs/index_'+str(i)+'.htm'

        getListUrl(url)
main()