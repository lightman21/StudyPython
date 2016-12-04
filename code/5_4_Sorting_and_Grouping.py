

'''
how to sort and group data use Python
'''

import json
import csv

def readDataAsList():
    filename = 'data/portfolio.csv'
    mlist = []
    with open(filename,'r') as f:
        #skip the title
        headers = next(f)
        data = csv.reader(f)
        for line in data:
            tdict = {
                    'name':line[0],
                    'date':line[1],
                    'shares':line[2],
                    'price':line[3]
                    }
            mlist.append(tdict)

        return mlist

def demo():
   portfolio = readDataAsList() 
   holding_name(portfolio[0])

   portfolio.sort(key=holding_name)
   print(portfolio)

   portfolio.sort(key=holding_price)
   print(portfolio)

   #use lambda
   portfolio.sort(key=lambda t : t['price'])
   portfolio.sort(key=lambda t : t['name'])

   min(portfolio.key = lambda t : t['date'])
   max(portfolio.key = lambda t : t['shares'])

   #group sth
   for name,items in itertools.groupby(portfolio,key=lambda holding : holding['name']):
       print('NAME',name)
       for it in items:
           print('  ',it)
            

   by_name = { name : list(items) 
       for name,items in itertools.groupby(portfolio,key=lambda holding : holding['name'])}



def holding_name(holding):
    return holding['name']

def holding_price(holding):
    return holding['price']

if __name__ == '__main__':
    demo()
