模拟登陆CSDN

url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
 
(1)F12
(2)选择连续日志（否则看不到之前post类型url）
(3)登录你的csdn，找到post类型的url
(4)参数里面有四个值（表单提交）,headers，cookie。。。。这些都是我们模拟登录需要的
(5)打开url的form，看到需要（流水号，还有一个值，_submit），前面两个值每次都会发生变动。因此，我们模拟登录必须要用到这两个值。
(6)设置cookie，获取上面的两个值。beautifulSoup过滤
(7)对提交的参数urlencode，headers ,cookie
(8)获得成功的代码


具体的网站需要具体的分析，这个过程并不是不变的，需要仔细观察登陆的数据



















