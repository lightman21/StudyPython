#! env /usr/bin/env python3
'''
use python-whois the module of the WHOIS protocol wrapper
install it via pip
pip install python-whois
'''
import sys
import whois 

def getOwner(url):
    data = whois.whois(url)
    print ('who is the owner of ',url)
    print data

if __name__ == '__main__':
    if len(sys.argv) == 2 :
        url = sys.argv[1]
        if url.startswith('http'):
            getOwner(url)
        else:
            raise SystemExit('url must startswith http')
    else:
        raise SystemExit('you must input url')
    









