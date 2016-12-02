'''
my first crawling program
so exciting ^_^
'''

import urllib2
import sys

def download(url,num_retries=2):
    print 'Downloading:',url
    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Downloading error:',e.reason
        html = None
        if num_retries > 0:
            #recursively retry 5XX HTTP errors
            return download(url,num_retries-1)

    return html

if __name__ == "__main__":
    if len(sys.argv) == 2:
           url = sys.argv[1]
           #url = 'http://www.google.com'
           data = download(url)
           print(type(data))
           print(data)



