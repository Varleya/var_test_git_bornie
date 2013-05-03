
import urllib2
from utils import *

class YahooDividend(object):
    def __init__(self, ticker, **args):
        if not ticker:
            raise Exception, "must supply stock symbol"
        self.qurl = "http://ichart.yahoo.com/table.csv?s=" + ticker
        self.start_date = args.get('start_date')
        self.end_date = args.get('end_date')

    def grab_data(self):
        # this later can be smarter about where data comes from
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        url = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=v&ignore=.csv" % \
            (self.qurl, (self.start_date.month-1), self.start_date.day, self.start_date.year \
            ,(self.end_date.month-1), self.end_date.day, self.end_date.year)
        
        #actually grab data
        raise Exception, parse_data(url)
        pdata = urllib2.urlopen(url)
        rows = pdata.readlines()
        # first row comes back with header, so to store just return everything after that
        pdata.close()
    