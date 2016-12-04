#! /usr/bin/env python3
#nextbus.py
#first python program so exciting^_^
import sys

if len(sys.argv) != 3 :
    raise SystemExit('Usage: nextbus.py rote stopid')

route = sys.argv[1]
stopid= sys.argv[2]

# route=22, stopid=14787 has data

import urllib.request

s = 'http://ctabustracker.com/bustime/map/getStopPredictions.jsp?route={}&stop={}'.format(route,stopid)
u = urllib.request.urlopen(s)
data = u.read()

import pdb; pdb.set_trace()     #just launch debugger

from xml.etree.ElementTree import XML
doc = XML(data)

for pt in doc.findall('.//pt'):
    print(pt.text)

