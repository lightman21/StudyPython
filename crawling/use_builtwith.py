'''
introduce the module  builtwith
first install through pip
pip install builtwith
'''
import builtwith
import sys

#! /usr/bin/env python3

def analysic(url):
   data = builtwith.parse(url)
   print(data)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1].startswith('http'):
        url = sys.argv[1]
        print url,'used technicals:'
        analysic(url)
    else:
        raise SystemExit('you need pass url or url must startswith http')

