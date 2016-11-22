2016-11-22 07:40
https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_01_03.html
很多时候运行python程序,需要类型这样
python3 nextbus.py
如果不想加前面的python3.可以这样
在nextbus.py的最上面加入
#! /usr/bin/env python3
以告诉系统这是一个python脚本,需要python3来执行
然后记得给这个nextbus.py加上可执行权限,即
chmod +x nextbus.py

在python程序中格式化或者说在字符串中动态取值可以这样
route = 100
stopid = 30
str = 'http://www.baidu.com/text.jsp?route={}&stop={}'.format(route,stopid)
这样就能把变量route和stopid的值替换到字符串str中

如果想要读取命令行的参数,需要导入一个module
import sys
在这个sys中有一个叫argv的数组封装了命令行传递的参数.
Caution index form one
argv[1]为第一个参数
如:python3 nextbus.py 22 1413
在代码中可以这样去获取
#22
first = sys.argv[1]
#1413
second = sys.argv[2]






































































