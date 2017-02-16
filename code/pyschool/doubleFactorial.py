import time

def doubleFact(num):
    product = 1
    i = 0
    k = product
    #caution num from input is a string 
    #you must convert it to a int or
    #in python int always less than string 
    while k <= int(num):
        k = i * 2 + 1
        product *= k
        i += 1
        print('i = {}, k = {}, num = {}, product = {},k <= num ={}'.format(i,k,num,product,(k <= num)))
        time.sleep(1)

    return product


import sys

if __name__ == '__main__':
    param = sys.argv[1]
    print('param = ',param)
    doubleFact(param)
