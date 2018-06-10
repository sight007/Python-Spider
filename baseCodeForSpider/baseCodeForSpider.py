import requests

url = "http://www.baidu.com"
try:
      r = requests.get(url)
      print r.status_code
      r.raise_for_status()
      r.encoding = r.apparent_encoding
      print r.text[:1000]
except:
      print "error"
      
