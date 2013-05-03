import stock
from datetime import timedelta

class Market(stock.Stock):
#	def __init__(self,ticker,*args):
#		super(Market, self).__init__()

    def grab_dividends(self, dates):
        if not dates:
            raise Exception, "you must supply dates for Market testing"
        self.div_dates = dates

    def grab_stock_data(self):
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        # bad way to do this but I'm going to force extra week of price data
        # to account for dividends on boundary
        start_date = self.start_date - timedelta(days=7)

        # qurl = "http://ichart.yahoo.com/table.csv?s=" + self.ticker
        import debug
        qurlt = "http://app.quotemedia.com/quotetools/getHistoryDownload.csv?&webmasterId=501&startDay=%s&startMonth=" + \
                "%s&startYear=%s&endDay=%s&endMonth=%s&endYear=%s&isRanged=false&symbol=%s" % (start_date.day, start_date.month \
                ,start_date.year, self.end_date.day, self.end_date.month, self.end_date.year, self.ticker)
        raise qurlt

        #qurlt = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=&q=q&y=0&z=%s&x=.csv" % \
        #        (self.qurl, (start_date.month-1), start_date.day, start_date.year \
        #        ,(self.end_date.month-1), self.end_date.day, self.end_date.year, self.ticker)

        self.tick_data = self.get_data(qurlt)