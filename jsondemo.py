'''
how to transform data to json
and transform data from json to Python's data structure
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
            tp = (line[0],line[1],line[2],line[3])
            mlist.append(tp)
        return mlist

def demo():
    data = readDataAsList()
    tojson = json.dumps(data)
    print("Python List to json:\n")
    print(tojson)
    print("\njson to Python:\n")

    data = json.loads(tojson)
    print("data type is ",type(data))
    print(data)

if __name__ == "__main__":
    demo()
