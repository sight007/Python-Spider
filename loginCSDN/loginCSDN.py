import urllib
import urllib2
import cookielib
from bs4 import BeautifulSoup

filename = 'cookie_csdn.txt'
cookie = cookielib.MozillaCookieJar(filename)
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

loginUrl = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'

response = opener.open(loginUrl)
soup = BeautifulSoup(response.read(),'lxml')
for input in soup.form.find_all('input'):
	if input.get('name') == 'lt':
		lt = input.get('value')
	if input.get('name') == 'execution':
		execution = input.get('value')
values = {
	'username':'249053957@qq.com',
	'password':'gzh249053957',
	'lt':lt,
	'execution':execution,
	'_eventId':'submit'
	}
opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; W…) Gecko/20100101 Firefox/56.0')]
postdata = urllib.urlencode(values)
result = opener.open(loginUrl, postdata)
cookie.save(ignore_discard=True, ignore_expires=True)

print result.read()











