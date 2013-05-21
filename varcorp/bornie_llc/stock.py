import urllib2
import datetime
from datetime import timedelta
import pickle
from utils import *
from googstock import GoogleIntradayQuote, GoogleQuote
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
        self.tdata = GoogleQuote(ticker, start_date=self.start_date, end_date=self.end_date)
        self.tdata.write_csv(('%s_ticker.csv') % ticker)
        self.tdata.write_csv_to_db(('%s_ticker.csv') % ticker, ticker)
        