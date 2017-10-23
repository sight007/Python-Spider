__author__ = 'GZH'

import urllib
import urllib2
import re
import sys
import os

#糗事百科爬虫类
class QSBK:

      #初始化一些参数
      def __init__(self):
            #默认的开始页码
            self.pageIndex = 1
            #需要拼接的url
            self.baseUrl = 'https://www.qiushibaike.com/hot/'
            #所有的内容，每页的内容作为元素
            self.allContent = []
            #请求头
            self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}
            #开关（输入一个值可以控制程序的关键）
            self.enable = True

      #获得某一页的编码
      def getPageCode(self, pageIndex):
            try:
                  url = self.baseUrl + str(pageIndex)
                  request = urllib2.Request(url, headers = self.headers)
                  response = urllib2.urlopen(request)
                  data = response.read().decode("utf-8")
                  #print data
                  return data
            except urllib2.URLError, e:
                  if hasattr(e, 'reason'):
                        print u'连接糗事百科失败，错误原因：', e.reason
                        return None
     
      #获得某一页想要的内容
      def getPageContent(self, pageIndex):
            regstr = u'<div class="article.*?>.*?<h2>(.*?)</h2>.*?<div class="content.*?<span>(.*?)</span>.*?<span class="stats.*?<i.*?>(.*?)</i>.*?<span class="stats.*?<i.*?>(.*?)</i>'
            pattern = re.compile(regstr,re.S)
            pageCode = self.getPageCode(pageIndex)
            items = re.findall(pattern,pageCode)
            #某一页的所有内容
            pageContent = []
            replaceBR = re.compile('<br/>')
            for item in items:
                  text = re.sub(replaceBR, "\n", item[1])
                  pageContent.append([item[0].strip(),text.strip(),item[2].strip(),item[3].strip()])
                  #print item[0].strip()
                  #print text.strip()
                  #print item[2].strip()
                  #print item[3].strip()
            return pageContent
      
      #加载并提取页面内容，加入到列表当中
      def loadPage(self):
            if self.enable == True:
                  if len(self.allContent) < 2:
                        pageContent = self.getPageContent(self.pageIndex)
                        if pageContent:
                              self.allContent.append(pageContent)
                              self.pageIndex += 1
      
      #输入值控制，得到某条段子        
      def getOneContent(self, pageContent, pageNum):
            for content in pageContent:
                  input = raw_input()
                  self.loadPage()
                  if input == 'Q':
                        self.enable = False
                        return
                  #注意：除了页数，需要点赞和评论数需要用%s
                  print u'第%d页\t发布人：%s\n发布内容:\n%s\n点赞%s\t评论%s' % (pageNum,content[0],content[1],content[2],content[3])

      #先加载了一页，存进allContent，取出allContent[0]作为参数，传进getOneContent（），页数+1，循环的输入开关控制输出
      #删除allContent的这条内容，保证allContent的长度始终为1
      def start(self):
            print u'正在读取糗事百科，按回车键查看新段子，Q退出'
            self.enable = True
            self.loadPage()
            nowPageNum = 0
            while self.enable:
                  if len(self.allContent) > 0:
                        pageContent = self.allContent[0]
                        nowPageNum += 1
                        del self.allContent[0]
                        self.getOneContent(pageContent, nowPageNum)

spider = QSBK()
spider.start()
