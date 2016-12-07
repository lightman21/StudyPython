'''
when request with urllib2 there is a default User-agent
I need change it
'''

import urllib2
import sys
import re

def crawl_sitmap(url):
    # download the sitmap file
    sitemap = download(url)
    #extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>',sitemap)
    print 'all links'
    print links,'size=',len(links),'\n'
    for link in links:
        # html = download(link)
        print 'try download: ',link



def download(url,user_agent='thstudy',num_retries=2):
    print 'Downloading:',url
    headers = {'User-agent':user_agent}

    # make a request with specify user-agent
    request = urllib2.Request(url,headers=headers)

    try:
        html = urllib2.urlopen(url).read()
    except urllib2.URLError as e:
        print 'Downloading error:',e.reason,'code=',e.code
        html = None
        if hasattr(e,'code') and e.code > 500 and e.code < 600:
            if num_retries > 0: #recursively retry 5XX HTTP errors
                print 'retry count',retries
                return download(url,num_retries-1)
            else:
                print 'retry finish'
                raise SystemExit('retry finish exit')
        else:
            print 'errcode: ' ,e.code
            raise SystemExit('other code error  exit!')
    
    
    return html

if __name__ == "__main__":
    if len(sys.argv) == 2:
           url = sys.argv[1]
           #url = 'http://www.google.com'
           crawl_sitmap(url)
           data = download(url)
           print 'data type is ',type(data)
           print(data)

