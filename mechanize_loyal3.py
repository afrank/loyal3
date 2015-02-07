#!/usr/bin/python

"""
This script uses mechanize and BeautifulSoup (bs4) to login to loyal3 and parse out existing stocks, 
their values, and quanities, and return them as a list of dictionaries. Extending this would be trivial.
"""

import os.path
import mechanize
import cookielib
from bs4 import BeautifulSoup
from pprint import pprint

creds = { 'username': 'YOUR_USERNAME_HERE', 'password': 'YOUR_PASSWORD_HERE' }

# comment this line out to disable use of a tmpfile (it's mostly just for testing)
# tmpfile = '/tmp/loyal3_index.tmp'

# Enable debugging. default is False.
# debug = True

def login(br,cj,link,creds):
    c = br.open(link)
    br.select_form(nr=1)
    br.form.find_control(id="username").value = creds['username']
    br.form.find_control(id="password").value = creds['password']
    br.submit()
    return br

# set some defaults
try:
    debug
except NameError:
    debug = None
try:
    tmpfile
except NameError:
    tmpfile = None

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

br.set_handle_equiv(True)
# enabling this produces a warning that gzip support is experimental,
# so only use it if you feel you must.
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

if debug is not None and debug == 1:
    br.set_debug_http(True)
    br.set_debug_redirects(True)
    br.set_debug_responses(True)

br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

if tmpfile is not None and os.path.isfile(tmpfile):
    print("using tmpfile %s") % (tmpfile,)
    html = open(tmpfile).read()
else:
    print("NOT using tmpfile")
    login(br,cj,'https://www.loyal3.com/login',creds)
    r = br.open('https://www.loyal3.com/accounts/index')
    html = r.read()

if tmpfile is not None:
    f = open(tmpfile,'w')
    f.write(html)
    f.close()

output = []
_html = BeautifulSoup(html)

for stock in _html.findAll('div', attrs={'class':'stockbox-expander'}):
    _org = stock.find('span', attrs={'class':'organization-name'}).text
    _ticker = stock.find('span', attrs={'class':'organization-ticker'}).text
    _owned = stock.find('span', attrs={'class':'shares_owned'}).text
    _cost = float(stock.find('span', attrs={'class':'price_per_share'}).text.replace('$',''))
    _total = float(stock.find('span', attrs={'class':'current_value'}).text.replace('$',''))
    output += [{'organization-name':_org, 'organization-ticker':_ticker, 'shares_owned':_owned, 'price_per_share':_cost, 'current_value':_total}]

pprint(output)

