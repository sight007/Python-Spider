import requests
import os 

url = "http://image.ngchina.com.cn/2018/0307/20180307050118889.jpg"
root = "D://北京理工爬虫课程图片"
path = root + url.split("/")[-1]

try:
      r = requests.get(url,timeout=30)
      r.raise_for_status()
      r.encoding = r.apparent_encoding
      if not os.path.exists(root):
            os.mkdir(root)
      if not os.path.exists(path):
            print "path" + path 
            with open(path,"wb") as f:
                  f.write(r.content)
                  f.close()
                  print u"a文件保存成功"
      else:
            print u"b文件已经存在"
except:
      print u"c请求网络出现问题！"
            
      
