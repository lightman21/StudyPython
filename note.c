

this is first txt I input through emacs.exciting.
2016-11-22 07:40
https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_01_03.html
很多时候运行python程序,需要类似这样
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

也可以判断sys.argv的长度.通过
if len(sys.argv) != 3 :
raise System.Exit('Something you wanna say)

注意这里的System.Exit()是退出程序的和Java的System.exit()差不多

在执行python程序的时候有一个很有用的选项 -i
如: python3 -i nextbus.py 22 14787
这会使你进入python的交互环境.你可以在里面打印出每一个变量的值
直接输入变量名回车即可.

在编写python代码的时候,可以通过如下方式打断点
在代码中插入snipet
import pdb; pdb.set_trace() #launch debugger就可以相当于打断点

在使用-i选项进入交互环境的时候,可以通过如下方式launch debugger
import pdb
这样以后就能launch debugger
    and then you input
pdb.pm()
    and you also can do do poking around like print sth
print(some)

    or you can get the program list just type  list

    or you can single-step through the code just type  s



    2016-11-23 07:35
    2.1 Project: Mortgage Calculator
    https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_02_01.html

    in Python we denote a statement body through the intent like

    while principle > 0 :
    month += 1
#do sth

    while age > 28
    print('old man')

    different intention means different statement

    and the if eles control flow works like this

    while principle > 0
    month += 1
    if month >= extra_payment_start_month and month <= extra_payment_end_month :
    total_payment = payment + extra_payment
    else :
    total_payment = payment
interest = principle * (rate / 12)

    that intersting.
    note that everything above belong a while loop
    because they are  all belong one intention
    and note the control flow, it must ends with a : marker
    like while xxx :   if xxx :   else :
    and in python there is a 'and' like Java's &&

    if you type python to enter the interactive interpreter
    and just type 1 + 2
    the output will be 3
    and next you want use the result last calculate 
    there is a _ ,which means the last calculate result
    then you can type like
    _ + 5
    and the result will be 8

    may be the output like this
    ------------------------------------------------------------
    ~/.vim/bundle(branch:th*) » python                                                                                                   
Python 2.7.12 (default, Oct 11 2016, 05:16:02)
    [GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 1 + 2
    3
    >>> _ + 5
    8
>>> quit()
    ------------------------------------------------------------

    2016-11-24 07:33
    2.2 Project formatted Output and File I/0
    https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_02_02.html
    about print()function output formatted,you can do like this
    name = 'IBM'
    shares = 100
    price = 23.2
    print('%10s %10d %10.2f' % (name,shares,price))
    or maybe you can do like
    print('{:>10s} {:>10d} {:>10.2f}'.format(name,shares,price))
    or maybe left align
    print('{:<10s} {:<10d} {:<10.2f}'.format(name,shares,price))

    >>> name = 'IBM'
    >>> shares = 100
    >>> price = 23.2
    >>> print('%10s %10d %10.2f' % (name,shares,price))
    IBM        100      23.20
    >>> print('{:>10s} {:>10d} {:>10.2f}'.format(name,shares,price))
    IBM        100      23.20
    >>> print('{:<10s} {:<10d} {:<10.2f}'.format(name,shares,price))
    IBM        100        23.20

# how to write the output to a file
    name = 'IBM'
    shares = 100
    price = 23.2

#open a file named schedules for writing
    out = open('schedules','w')
    print('{:<10s} {:<10d} {:<10.2f}'.format(name,shares,price),file=out)
#after your writing you should close it
out.close()

    2016-11-25 07:50
    3.1 File and String Basic
    https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_03_01.html


n 3.5.2 (default, Oct 11 2016, 05:00:16) 
    [GCC 4.2.1 Compatible Apple LLVM 7.0.2 (clang-700.1.81)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> f = open('mytest.csv','r')
    >>> f
    <_io.TextIOWrapper name='mytest.csv' mode='r' encoding='UTF-8'>
>>> data = f.read()
    >>> data
    '"AA"\t"6/11/07"\t100\t    32.20\n"IBM"\t"5/13/07"\t50      91.10\n"CAT"\t"9/23/06"\t150\t    83.44\n"MSFT"\t"5/17/07"\t200\t    51.23\n"GE"\t"2/1/06"\t95\t    40.37\n"MSFT"\t"10/31/06"\t50\t    65.10\n"IBM"\t"7/9/06"\t100 \t70.44\n'
>>> print(data)
    "AA"    "6/11/07"   100     32.20
    "IBM"   "5/13/07"   50      91.10
    "CAT"   "9/23/06"   150     83.44
    "MSFT"  "5/17/07"   200     51.23
    "GE"    "2/1/06"    95      40.37
    "MSFT"  "10/31/06"  50      65.10
    "IBM"   "7/9/06"    100     70.44

>>> f.close()
    >>> f  = open('mytest.csv','r')
    >>> for line in f:
...     print(line)
    ... 
    "AA"    "6/11/07"   100     32.20

    "IBM"   "5/13/07"   50      91.10

    "CAT"   "9/23/06"   150     83.44

    "MSFT"  "5/17/07"   200     51.23

    "GE"    "2/1/06"    95      40.37

    "MSFT"  "10/31/06"  50      65.10

    "IBM"   "7/9/06"    100     70.44

    >>> line
    '"IBM"\t"7/9/06"\t100 \t70.44\n'
>>> f.close()
    >>> with open('mytest.csv','r') as f:
...     data = f.read()
    ... data
    File "<stdin>", line 3
    data
    ^
    SyntaxError: invalid syntax
    >>>     data
    File "<stdin>", line 1
    data
    ^
    IndentationError: unexpected indent
>>> print(data)
    "AA"    "6/11/07"   100     32.20
    "IBM"   "5/13/07"   50      91.10
    "CAT"   "9/23/06"   150     83.44
    "MSFT"  "5/17/07"   200     51.23
    "GE"    "2/1/06"    95      40.37
    "MSFT"  "10/31/06"  50      65.10
    "IBM"   "7/9/06"    100     70.44

    >>> 
    >>> line
    '"IBM"\t"7/9/06"\t100 \t70.44\n'
>>> line=line.strip()
    >>> 
    >>> a = 'hello world'
    >>> a
    'hello world'
    >>> b = "hello world"
    >>> b
    'hello world'
    >>> a[0]
    'h'
    >>> a[-1]
    'd'
    >>> a[-3]
    'r'
    >>> a[0:5]
    'hello'
    >>> a[:5]
    'hello'
    >>> a[-5:]
    'world'
    >>> line
    '"IBM"\t"7/9/06"\t100 \t70.44'
    >>> line[1:4]
    'IBM'
>>> len(line)
    25
>>> len(a)
    11
    >>> c = 'hello' + 'world'
    >>> c+b
    'helloworldhello world'
    >>> line
    '"IBM"\t"7/9/06"\t100 \t70.44'
    >>> 

>>> line.strip()
    '"IBM"\t"7/9/06"\t100 \t70.44'
>>> line = line.strip()
    >>> line
    '"IBM"\t"7/9/06"\t100 \t70.44'
    >>> line.replace('"','-')
    '-IBM-\t-7/9/06-\t100 \t70.44'
    >>> parts=line.split('\t')
    >>> parts
    ['"IBM"', '"7/9/06"', '100 ', '70.44']
    >>> parts[0]
    '"IBM"'
    >>> parts[1]
    '"7/9/06"'
    >>> parts[0] = parts[0].strip('"')
    >>> parts[0]
    'IBM'
    >>> parts[2] * parts[3]
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    TypeError: can't multiply sequence by non-int of type 'str'
    >>> parts[2]=int(parts[2])
        >>> parts[3]=float(parts[3])
        >>> parts
        ['IBM', '"7/9/06"', 100, 70.44]
        >>> mul=parts[2] * parts[3]
        >>> mul
        7044.0
        >>> 

        2016-11-26 09:30
        http://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_03_02.html
        3.2 Reading form a file and Performing a Calculation

        write a little program port.py

        when you open a file you must close it
    f = open('/a/b/c.txt','r')
    f.read()
f.close()

    but with 'with' python can auto close for you
    with open('/a/b/c.txt','r') as f :
    do sth

    2016-11-27  09:39
    https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_03_03.html
    3.3 Using the cvs Module to Read Data
    caution:
    there is no i++ in Python
    your can only do this by type i += 1

    in Python we do cast like this
int t = int(var)
    but in Java thing is
    int j = (int)var

    2016-11-28  13:25
    http://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_04_01.html
    4.1 Defining and using a simple function

    def add(a,b):
        return a+b

    the interesting is when you using this function,you can
use it like add(a = 10,b = 3) or add(10,8),add(10,b=30)
    but you can't use like add(a=10,8)
    when you us function's argument,the argument must be the last 

    there is a help(functionname) function in Python .
    when you don't know how to use a function.like add()
    you just type help(add) for get sth


    also introduce a module called glob
    it's used to grep some files like grep
    import glob
    files = glob.glob('data/portfolio*.csv')
    for file in files:
print(file)

    >>> import glob
    >>> files = glob.glob('portfo*.csv')
    >>> files
    ['portfolio.csv', 'portfolio2.csv']
    >>> for file in files:
...     print(file)
    ...
    portfolio.csv
    portfolio2.csv
    >>>


    2016-11-29 08:20 
    4.3 Handling bad Data and Exception Handling
    https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_04_03.html

    Python handle exception
    ValueError is like Java's Exception

    try:
    row[2] = int(row[2])
row[3] = float(row[3])
    except ValueError as err:
    print('Row: ',rowno, 'Bad row: ',row)
    continue

    and also introduce enumerate,usage like this

    with open(filename,'r') as f:
rows = csv.reader(f)
    headers = next(rows)    #skip the header row
    for rowno,row in enumerate(rows,start=1):
# now you can use rowno
# Python will autoinitialize and autoincrement it for you

        2016-11-30 08:00
        https://www.safaribooksonline.com/library/view/python-programming-language/9780134217314/PYMC_04_04.html

        what does the * mean when it appear in function define? like
        def greeting(name,*,where):
        sth...

        generally,you may be want check the parameter passed to function like

        def portfolio_cost(name,error):
            if error not in {'silent','warn','raise'} :
            raise ValueError("error must be one of 'warn','silent','raise'")

            and you can force the client who invoke your function to pass solid params like
            def portfoli_cost(name,*,errors='warn'):
#do sth
                this means if the client pass just one parameter,you give it a default parameter
                and if the client pass two, it must use this way 
                portfolio(name,errors='silent'):
#do sth

                    when you handle an error,like open a file but with a bad name
                    why you don't cover this?
                    never cath error unless you can actually deal with the error
                    because there is not actually recovery options for a bad file .
                    it doesn't make sense with a bod name recovery.
                    so in terms of writing this code,you just ignore it.
                    if your code is crashing with that exception that
                    beyond your control,it's often better to let the program crash.


                    when you want format float  you can do like this
# 2 digital decimal plate
                    a = 1.0
                    a = '%.2f' % a

                    2016-12-01 12:30
                    5.1 Basic Material: Tuples,List,Set,and Dictionary

                    define a tuple
                    t = ('AA','2011-06-07',100,32.2)
                    a tuple is like a immutable array

                    maybe tuple used to packing and unpacking data
                    things like this is packing data
                    t = ('AA','2011-06-07',100,32.2)

                    and the unpacking is

                    name,data,shares,price = t

                    then you get these variable initialized
                    name = 'AA'
                    data = '2011-06-07'
                    and so on

                    List
                    define a list
                    names = ['IBM','YAHOO','CAT']
                    the different between tuple and list
                    1.tuple defined by () but list defined by []
                    2.tuple is immutable but list is mutable 

                    Set
                    define a set
                    mset = {1,2,2,1}

                    sometimes, you can check if a sth in the mset like

                    a in mset

                    dictionary(like Java's map)
                    define a dictionary
                    the defination of a dictionary is like a Java's JSONObject's toString()

                    mdic = {'a':100,'b':200}



                    2016-12-02 08:00
                    5.2 Build a Data Structure from a file

                    reread portfolio.csv as a list
                    maybe as a list of tuple
                    and when in the for loop you need unpacking the tuple
                    but what if where's 25 variables in a tuple
                    so you need to reread the data as a list of dictionary

                    when you need communication to another language maybe the data structure
                    will be json. and Python built-in a module called json
    import json
jsondata = json.dumps(listInPython)
    now you get the json data
    and when you wanna read the json data to Python Data Structure
listInPython = json.loads(jsondata)

    when you in a python file
    when there are more than one function
    which one is the main or how you can specific invoke which function?

# like Java's main() method ?
    if __name__ == "__main__":
# now choose which one you need perform first

    2016-12-03 09:00
    5.3 Data Manipulation

    introduce the usage of there base on the protfolio.csv data
    comprehension for loop
    usage for these function
    zip()
    sum()
    set()
    dict()
    and string's join()
    
examples:

    String's join() function
    suppose you have a list like 
    and you wanna get a string like 1_2_3_4
    ['a', 'b', 'c']
    '_'.join(list)
    'a_b_c'

    suppose you have a list type of dictionary tlist like 
    tlist = 
[
    {'date': '2007-06-11', 'price': '32.20', 'name': 'AA', 'shares': '100'},
    {'date': '2007-05-23', 'price': '91.10', 'name': 'IBM', 'shares': '50'},
    {'date': '2006-09-23', 'price': '83.44', 'name': 'CAT', 'shares': '150'},
    {'date': '2007-05-17', 'price': '51.23', 'name': 'MSFT', 'shares': '200'},
    {'date': '2006-02-01', 'price': '40.37', 'name': 'GE', 'shares': '95'},
    {'date': '2006-10-31', 'price': '65.10', 'name': 'MSFT', 'shares': '50'},
    {'date': '2006-07-09', 'price': '70.44', 'name': 'IBM', 'shares': '100'}
]
# you can use do this
listnames = [ item['name'] for item in tlist ]

#and if you have duplicate data you can use set() to remove it like
unique_names = set(listnames)

#and if you wanna get all price in a list
prices = [item['price'] for item in tlist]

#interesting zip() function for pairs things like this 
names
['AA', 'IBM', 'CAT', 'MSFT', 'GE', 'MSFT', 'IBM', 'TTTTT']
>>> prices
['32.20', '91.10', '83.44', '51.23', '40.37', '65.10', '70.44']
>>>

#you can remove duplicate name like caustion the curly brace
#that Python will know you wanna use a set
names = { name for name in names }

#you may wanna prices to be all float
prices = { float(price) for price in prices }

#pairs names and prices
for name price in zip(names,prices):
    print(name,'=',price)

or may be you wanna a dictionary
name_price_pairs = dict(zip(names,prices))

#make a simple request
import urllib.request

url = 'http://finance.yahoo.com/d/quotes.csv?s={}&f=l1'.format(namestr)'
u = urllib.request.urlopen(url)
data = u.read()

print(data)
b'95.14\n160.02\n31.34\n29.04\n59.25\n'
>>> type(data)
<class 'bytes'>
>>> data = data.split()
>>> data
[b'95.14', b'160.02', b'31.34', b'29.04', b'59.25']
>>> type(data)
<class 'list'>
>>>

bytes to list call bytes's split() function


  2016-12-04 11:20
   5.4 Example:Sorting and Grouping
    how to sort the list of dictionary
    introduce Python lambda
    built-in function min() max()

Material: you have a list of dictionary like

   tlist = 
[
   {'date': '2007-06-11', 'price': '32.20', 'name': 'AA', 'shares': '100'},
   {'date': '2007-05-23', 'price': '91.10', 'name': 'IBM', 'shares': '50'},
   {'date': '2006-09-23', 'price': '83.44', 'name': 'CAT', 'shares': '150'},
   {'date': '2007-05-17', 'price': '51.23', 'name': 'MSFT', 'shares': '200'},
   {'date': '2006-02-01', 'price': '40.37', 'name': 'GE', 'shares': '95'},
   {'date': '2006-10-31', 'price': '65.10', 'name': 'MSFT', 'shares': '50'},
   {'date': '2006-07-09', 'price': '70.44', 'name': 'IBM', 'shares': '100'}
]

TODO:
   how to write a list of dictionry to a file

# you wanna to sort that data by any key of the dictionary
sort by name
sort by price

def holding_name(holding):
   return holding['name']

and also introduce Python's lambda to simpilify the simple function
a = lambda x : 10 * x
a(10)
b = lambda x,y : x + y
b(2,3)

portfolio.sort(key = lambda holding : holding['shares'])

min(portfolio,key = lambda holding : holding['price'])

max(portfolio,key = lambda holding : holding['name'])

group data

import itertools

for name,items in itertools.groupby(portfolio, key = lambda holding : holding['name']):
   print('NAME',name)
       for it in items:
           print('     ',it)

by_name = { name: list(items)
           for name, items in itertools.groupby(portfolio, key = lambda holding : holding['name'])}

#give me the enties of IBM
by_name('IBM')



  2016-12-05 22:48 
    6.1 Module Basic

    when you want use some function in others.you need to import it.
    like import cvs.
    the way you load it and run it is import.
    by doing so in Python Interceptor env
    import csv
    csv
    #now you will see the detail of csv module
    mdule 'csv' from '/usr/local/Cellar/python/2.7.12_2/Frameworks/Python.framework/Versions/2.7/lib/python2.7/csv.pyc'>
    
   when Python execute where Python will find the code?
   import sys
   sys.path

   when you import a module,Python will cache it,which means
    
    #imagine there is a module called simple

   '''
   this is a simple file called simple.py used to illustrate module import sth
   # simple.py start

    x = 42

    def spam():
        print('x is ',x)

    def run():
        print('Calling spam')
        spam()

    print('Running')
    run()

    #Pretty like Java's main() method

    if __name__ == 'main__':
        run()

   # simple.py end
   '''

    from simple import run
    
    when you does like: import module
    Python will cache the module 
    which means when you rerun import module
    something not happend like you just first import it
    but you also can delete your import by:
    del sys.modules['what_your_module_name']
    and then when you reimport by
    import xxx 
    things gonna happen again

    when you use library which means you use import a module
    like Java's main() method  Python has an entry point
    you can use it to specify what you wanna go first
    through:
    if __name__ == '__main__':
        # call your function here

    and when your .py file doesn't specify the __name__ 
    default your __name__ is your file name.
    for example when you are in terminal and you just type
    Python myfile.py
    when Python execute your myfile.py,the __name__ is  myfile




































































