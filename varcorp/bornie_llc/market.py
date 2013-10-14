from datetime import timedelta
import urllib2

class Market(object):

    def grab_stock_data(self, symbol="%SEDJI"):
        start_date = "01-01-2000"
        end = "05-21-2013"
        url = "http://www.tr4der.com/download/historical-prices/{0}/from-{1}-to-{2}/".format(symbol, start, end)
    
        mdata = urllib2.urlopen(url)
        rows = mdata.readlines()
