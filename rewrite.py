'''
reread data from portfolio.csv and return a list of them

        name,date,shares,price
        "AA","2007-06-11",100,32.20
        "IBM","2007-05-23",50,91.10
        "CAT","2006-09-23",150,83.44
        "MSFT","2007-05-17",200,51.23
        "GE","2006-02-01",95,40.37
        "MSFT","2006-10-31",50,65.10
        "IBM","2006-07-09",100,70.44
'''

import json
import sys
import csv

filename = 'data/portfolio.csv'
def readcsv(filename):
    mlist = []
    with open(filename,'r') as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
             #packing a tuple
             tp = (row[0],row[1],row[2],row[3])
             mlist.append(tp)

#unpacking
    for name,date,shares,price in mlist:
        print(name,date,price)

def readAsList(filename):
    mlist = []
    with open(filename,'r') as ff:
        data = csv.reader(ff)
#       name,date,shares,price
        for line in data :
            dic = {
                    'name': line[0] ,
                    'date':line[1],
                    'shares':line[2],
                    'price':line[3]
                  }

            mlist.append(dic)

        return mlist

# like Java's main() ?
if __name__ == "__main__":
    filename = 'data/portfolio.csv'
    tlist = readAsList(filename)
    print("list of dictionary")
    print(tlist)
    #sth to json
    jsondata = json.dumps(tlist)
    print("json dumps")
    print(jsondata)
    #json to Python
    tlist = json.loads(jsondata)
    print(len(tlist))

