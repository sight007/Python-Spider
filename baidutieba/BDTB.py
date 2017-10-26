__author__ = 'GZH'

import urllib
import urllib2
import re
import tool

class BDTB:
      
      def __init__(self, baseUrl, seeLZ):
            self.baseUrl = baseUrl
            self.seeLZ = '?see_lz=' + str(seeLZ)
            
      def getPageCode(self, pageNum):
            try:
                  url = self.baseUrl + self.seeLZ + '&pn=' +str(pageNum)
                  request = urllib2.Request(url)
                  response = urllib2.urlopen(request)
                  pageCode = response.read()
                  #print pageCode
                  return pageCode
            except urllib2.URLError, e:
                  if hasattr(e, 'reason'):
                        print u'连接百度贴吧失败，错误原因：', e.reason
                        return None

      def getTitle(self):
            firstPageCode = self.getPageCode(1)
            regTitle = '<h3 class="core_title_txt.*?>(.*?)</h3>'
            pattern = re.compile(regTitle, re.S)
            result = re.search(pattern, firstPageCode)
            if result:
                  #print result.group(1)
                  return result.group(1).strip()
            else:
                  return None

      def getPageNum(self):
            firstPageCode = self.getPageCode(1)
            regNum = '<li class="l_reply_num.*?red">(.*?)</span>'
            pattern = re.compile(regNum, re.S)
            result = re.search(pattern, firstPageCode)
            if result:
                  #print result.group(1)
                  return result.group(1).strip()
            else:
                  return None

      def saveImg(self, imgUrl, fileName):
            u = urllib.urlopen(imgUrl)
            data = u.read()
            f = open(fileName, 'wb')
            f.write(data)
            f.close()
      
      def saveImgs(self, pageCode, pageNum):
            print 'download your pictures。。。。'
            regImg = '<img class="BDE_.*?src="(.*?)".*?>'
            pattern = re.compile(regImg, re.S)
            imgUrls = re.findall(pattern, pageCode)
            number = 1
            for imgUrl in imgUrls:
                  splitPath = imgUrl.split('.')
                  fTail = splitPath.pop()
                  if len(fTail) == 3:
                        fTail = "jpg"
                        fileName = str(pageNum) + str(number) + "." + fTail
                        self.saveImg(imgUrl,fileName)
                  number += 1

                            
      def getContent(self, pageNum):
            if pageNum < self.getPageNum():
                  pageCode = self.getPageCode(pageNum)
                  regContent = '<div id="post_content_.*?>(.*?)</div>'
                  pattern = re.compile(regContent, re.S)
                  items = re.findall(pattern, pageCode)
                  self.saveImgs(pageCode, pageNum)
                  atool = tool.Tool()
                  file = open("top50.txt","w+")
                  for item in items:
                        aitem = atool.replace(item)
                        file.write(aitem)
                        if len(aitem) < 500:
                              continue
                        print aitem
                        #print len(aitem)
                        print u'-----------------这是次元壁-----------------------'
            else:
                  print '超过最大页数，请重新输入'
            
      def selectPageNum(self):
            while True:
                  pageNum = input('请输入页码，输入0退出:\n')
                  if pageNum == 0:
                        print '程序退出。。。。'
                        break
                  print '-----------------------下面是内容-----------------------------'
                  self.getContent(pageNum)
                  
baseURL = 'https://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
print '标题：', bdtb.getTitle()
print '页数：', int(bdtb.getPageNum())
bdtb.selectPageNum()
