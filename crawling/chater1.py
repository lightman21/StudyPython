#! env /usr/bin/env python3
'''
when request with urllib2 there is a default User-agent
I need change it
'''

import urllib2
import sys
import re
import itertools
import urlparse


#maximum number of consecutive download errors allowed
max_errors = 5

def iteraterID():
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' % page
        html = download(url)
        if html is None:
            #now received an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                #reached maximum number of counsecutive errors so exit
                raise SystemExit('reached maximum errors')
            else:
                #success -can scrape the result
                num_errors = 0

def link_crawler(seed_url,link_regex):
    '''
        Crawl from the given seed URL following links matched by link_regex
    '''
    crawl_queue = [seed_url]
    # keep track which URL's have seen before
    seen = set(crawl_queue)

    while   crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        #filter for links matching our regular expression
        for link in get_links(html):
            if re.match(link_regex,link):
                link = urlparse.urljoin(seed_url,link)
                #check if have already seen this link
                if link not in seen:
                    crawl_queue.append(link)

def get_links(html):
    '''
    return a lst of links from html
    '''
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']',re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

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
#           crawl_sitmap(url)
#           data = download(url)
#           print 'data type is ',type(data)
#           print(data)
    elif len(sys.argv) == 3:
        url = sys.argv[1]
        reg = sys.argv[2]
        link_crawler(url,reg)


