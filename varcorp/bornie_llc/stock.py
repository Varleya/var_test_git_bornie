import urllib2
import datetime
from datetime import timedelta
import pickle
from utils import *
from googstock import GoogleIntradayQuote
from yahoostock import YahooDividend


class Stock(object):
    """stock module has dividend sub classes but also holds price tick data for itself"""
    def __init__(self, ticker, **args):
        super(Stock, self).__init__()
        self.ticker = ticker
        self.start_date = args.get('start_date')
        self.end_date = args.get('end_date')
        #self.tick_data = GoogleIntraDay()
        self.dividends = YahooDividend(ticker, start_date=self.start_date, end_date=self.end_date).grab_data()
        num_days = (self.end_date-self.start_date).days
        self.tdata = GoogleIntradayQuote(ticker, num_days=num_days).write_csv('GE_ticker.csv')
        self.qurl = "http://ichart.yahoo.com/table.csv?s=" + ticker




    def get_data(self, url):
        nodata = True
        urlkey = ""
        keys, rows = self.grab(url)
        if not keys:
            print url
            raise Exception, "BAD URL...maybe"
        data = {}
        for row in rows[1:]:
            row = parse_single_entry(row)
            data[row[0]] = dict(zip(keys[1:], row[1:]))        
        return data

    def grab_stock_data(self):
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        # bad way to do this but I'm going to force extra week of price data
        # to account for dividends on boundary
        start_date = self.start_date - timedelta(days=7)

        # qurl = "http://ichart.yahoo.com/table.csv?s=" + self.ticker
        qurlt = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=&q=q&y=0&z=%s&x=.csv" % \
                (self.qurl, (start_date.month-1), start_date.day, start_date.year \
                ,(self.end_date.month-1), self.end_date.day, self.end_date.year, self.ticker)

        self.tick_data = self.get_data(qurlt)

    def grab_dividends(self):
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        qurlt = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=v&ignore=.csv" % \
            (self.qurl, (self.start_date.month-1), self.start_date.day, self.start_date.year \
            ,(self.end_date.month-1), self.end_date.day, self.end_date.year)
        
        self.div_data = self.get_data(qurlt)
        self.div_dates = self.div_data.keys()

    # want to move this at some point
    def price_delta(self):
        price_deltas = []
        for date in self.div_dates:
            # check for monday ex-dates...further analysis done later.
            days = self.valid_date(date)

            sell = date
            buy = sell - timedelta(days=days)
            pdelta = (self.tick_data[sell]['Open']-self.tick_data[buy]['Close'])
            price_deltas.append(pdelta)
        return price_deltas

    def price_yield(self, selltime):
        yields = []
        for date in self.div_dates:
            days = self.valid_date(date)

            sell = date
            buy = sell - timedelta(days=days)
            try:
                pyields = (self.tick_data[sell][selltime]-self.tick_data[buy]['Close']) / self.tick_data[buy]['Close']
                yields.append(pyields)
            except:
                pass
        return yields

    def div_yield(self):
        yields = []
        for date in self.div_dates:
            days = self.valid_date(date)    

            sell = date
            buy = sell - timedelta(days=days)
            dyields = (self.div_data[sell]['Dividends']/self.tick_data[buy]['Close'])
            yields.append(dyields)
        return yields

    def valid_date(self, date):
        days = 0
        while True:
            days += 1
            try:
                self.tick_data[date - timedelta(days=days)]
            except KeyError, OverflowError:
                continue
            return days
