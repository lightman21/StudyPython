'''
read data from /data/portfolio.csv and return a list of them
'''
with open('/data/portfolio.csv','r') as f:
    data = f.read()
    print(data)
