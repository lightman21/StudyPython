import csv
import json

def readDataAsList():
    filename = 'data/portfolio.csv'
    mlist = []
    with open(filename,'r') as f:
        #skip the title
        headers = next(f)
        data = csv.reader(f)
        for line in data:
            dic = {
                    'name':line[0],
                    'date':line[1],
                    'shares':int(line[2]),
                    'price':float(line[3])
                    }
            mlist.append(dic)
        return mlist

def useforLoop():
    mlist = readDataAsList()

    tlist = []
    for it in mlist:
        tlist.append(it['name'])
    #print(tlist)

    #simple syntax
#    total = sum([item['shares'] * item['price'] for item in mlist])
#    print(total)

    mset = set(item['price'] for item in mlist)
    #print(mset)    

    more40 = [holding for holding in mlist if holding['price'] > 40]
    #print('more40=',more40)

    #tell python return a list
    names = [item['name'] for item in mlist]
    unique_names = set(names)

    #tell python return a set
    #setname = { item for item in mlist }
    #print(type(setname),setname)

    # join usage
    namestr = ','.join(unique_names)
    print(namestr)

    import urllib.request
    url = 'http://finance.yahoo.com/d/quotes.csv?s={}&f=l1'.format(namestr)
    #http://finance.yahoo.com/d/quotes.csv?s=CAT,AA,GE,MSFT,IBM&f=l1
    u = urllib.request.urlopen(url)
    data = u.read()
    print(data)
    pricedata = data.split()

    # pairs unique_names and pricedata use zip() function
    for name,price in zip(unique_names,pricedata):
        print(name,'=',price)

    # make a dictionary
    pricedic = dict(zip(unique_names,pricedata))
    print(pricedic)

    prices = { name:float(price) for name,price in zip(unique_names,pricedata) }
    print(prices)

if __name__ == "__main__":
        useforLoop()

