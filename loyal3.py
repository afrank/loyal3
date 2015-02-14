#!/usr/bin/python

"""
This class uses mechanize and BeautifulSoup (bs4) to login to loyal3 and parse out existing stocks, 
their values, and quanities, and return them as a list of dictionaries. Extending this would be trivial.
"""

import os.path
import mechanize
import cookielib
from bs4 import BeautifulSoup
import ConfigParser

class Loyal3:
    def __init__(self):
        # abstract the credentials to make it easier to store in git. if you want to remove a dependency,
        # you can just hard-code the creds here
        self.creds_file = '/home/afrank/creds.ini'
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(self.creds_file))
        self.creds = { 'username': self.config.get('loyal3','username'), 'password': self.config.get('loyal3','password') }
        self.debug = False
        self.tmpfile = None
        self.logged_in = False

        # comment this line out to disable use of a tmpfile (it's mostly just for testing)
        # self.tmpfile = '/tmp/loyal3_index.tmp'

        # Enable debugging. default is False.
        # self.debug = True

        self.br = mechanize.Browser()
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        self.br.set_cookiejar(self.cj)

        self.br.set_handle_equiv(True)
        # enabling this produces a warning that gzip support is experimental,
        # so only use it if you feel you must.
        #self.br.set_handle_gzip(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # set our user-agent
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    def debug(self,v):
        self.br.set_debug_http(v)
        self.br.set_debug_redirects(v)
        self.br.set_debug_responses(v)

    def login(self):
        c = self.br.open('https://www.loyal3.com/login')
        self.br.select_form(nr=1)
        self.br.form.find_control(id="username").value = self.creds['username']
        self.br.form.find_control(id="password").value = self.creds['password']
        self.br.submit()
        self.logged_in = True
        #return br
        return True

    def get_stocks(self):
        self.login()
        r = self.br.open('https://www.loyal3.com/accounts/index')
        html = r.read()
        output = []
        _html = BeautifulSoup(html)
        output = []
        _html = BeautifulSoup(html)

        for stock in _html.findAll('div', attrs={'class':'stockbox-expander'}):
            _org = stock.find('span', attrs={'class':'organization-name'}).text
            _ticker = stock.find('span', attrs={'class':'organization-ticker'}).text.replace('(','').replace(')','')
            _owned = stock.find('span', attrs={'class':'shares_owned'}).text
            _cost = float(stock.find('span', attrs={'class':'price_per_share'}).text.replace('$',''))
            _total = float(stock.find('span', attrs={'class':'current_value'}).text.replace('$',''))
            output += [{'organization-name':_org, 'organization-ticker':_ticker, 'shares_owned':_owned, 'price_per_share':_cost, 'current_value':_total}]
        return output

# disabled tmpfile support for now

#if tmpfile is not None and os.path.isfile(tmpfile):
#    print("using tmpfile %s") % (tmpfile,)
#    html = open(tmpfile).read()

#if tmpfile is not None:
#    f = open(tmpfile,'w')
#    f.write(html)
#    f.close()

