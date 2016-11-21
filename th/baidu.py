import urllib.request

s = 'http://www.baidu.com'
u = urllib.request.urlopen(s)
data = u.read()
print(data)
