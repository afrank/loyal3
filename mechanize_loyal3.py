#!/usr/bin/python

from loyal3 import Loyal3
import monitoring2_7
from pprint import pprint

L = Loyal3()

output = L.get_stocks()

g = monitoring2_7.Graphite()
g.set_prefix("afrank.stocks")

for s in output:
    g.add("%s.shares_owned" % s['organization-ticker'], s['shares_owned'])
    g.add("%s.price_per_share" % s['organization-ticker'], s['price_per_share'])
    g.add("%s.current_value" % s['organization-ticker'], s['current_value'])

g.send('127.0.0.1')
#pprint(output)
