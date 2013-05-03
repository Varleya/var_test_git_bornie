import urllib2
import datetime
from datetime import timedelta
import pickle

def parse_header(line):
    # parse single line by delimter
    row = []
    cells = line.split(',')
    for cell in cells:
        # get rid of new line
        cell = cell.strip()
        row.append(cell)
    return row

def parse_single_entry(line):
    # parse single line by delimter
    row = []
    cells = line.split(',')
    datecol = True
    for cell in cells:
        # get rid of new line
        cell = cell.strip()
        if datecol:
            date = datetime.datetime.strptime(cell, "%Y-%m-%d")
            datecol = False
            row.append(date)
            continue
        row.append(float(cell))
    return row

def parse_data(url):
    pdata = urllib2.urlopen(url)
    rows = pdata.readlines()
    pdata.close()
    tick_data = {}
    keys = parse_header(rows[0])

    for row in rows[1:]:
        row = parse_single_entry(row)
        tick_data[row[0]] = dict(zip(keys[1:], row[1:]))
    
    return tick_data

class Stock(object):
    """stock module has dividend sub classes but also holds price tick data for itself"""
    def __init__(self, ticker, *args):
        super(Stock, self).__init__()
        self.ticker = ticker
        self.start_date = None
        self.end_date = None
        self.tick_data = {}
        self.div_data = {}
        self.qurl = "http://ichart.yahoo.com/table.csv?s=" + self.ticker
        self.market = {}

    def grab_index(self, market='^DJI'):
        self.market = self.grab_stock_data(self, market)
        

    def grab(self, url):
        # actual internet piece that will later look at dB for existence
        try:
            pdata = urllib2.urlopen(url)
            rows = pdata.readlines()
            pdata.close()
            keys = parse_header(rows[0])
            return keys, rows
        except:
            print url
            return [],[]
        

    def get_data(self, url):
        nodata = True
        urlkey = ""
        #for i in url:
        #    urlkey += str(ord(i))
        #try:
        #    data = pickle.load(open(urlkey,"rb"))
        #    return data
        #except:
        #    # no data yet or other error
        #    pass
        keys, rows = self.grab(url)
        data = {}
        for row in rows[1:]:
            row = parse_single_entry(row)
            data[row[0]] = dict(zip(keys[1:], row[1:]))
        
        #pickle.dump(data, open(urlkey, "wb"))
        return data

    def grab_stock_data(self, url_over=None):
        url_over = self.qurl if not url_over else url_over
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        # bad way to do this but I'm going to force extra week of price data
        # to account for dividends on boundary
        start_date = self.start_date - timedelta(days=7)

        # qurl = "http://ichart.yahoo.com/table.csv?s=" + self.ticker
        qurlt = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=&q=q&y=0&z=%s&x=.csv" % \
                (url_over, (start_date.month-1), start_date.day, start_date.year \
                ,(self.end_date.month-1), self.end_date.day, self.end_date.year, self.ticker)

        self.tick_data = self.get_data(qurlt)



    def grab_dividends(self):
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        qurlt = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=v&ignore=.csv" % \
            (self.qurl, (self.start_date.month-1), self.start_date.day, self.start_date.year \
            ,(self.end_date.month-1), self.end_date.day, self.end_date.year)
        
        self.div_data = self.get_data(qurlt)

    def price_delta(self):
        price_deltas = []
        for i, date in enumerate(self.div_data.keys()):
            # check for monday ex-dates...further analysis done later.
            days = self.valid_date(date)

            sell = date
            buy = sell - timedelta(days=days)
            pdelta = (self.tick_data[sell]['Open']-self.tick_data[buy]['Close'])
            price_deltas.append(pdelta)
        return price_deltas

    def price_yield(self, selltime):
        yields = []
        for i, date in enumerate(self.div_data.keys()):
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
        for i, date in enumerate(self.div_data.keys()):
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

    def printy(self):
        import debug
        sum_pnl =0
        for i, date in enumerate(self.div_data.keys()):

            days = 1
            # check for monday ex-dates...further analysis done later.
            if date.weekday() == 0: 
                days = 3


            sell = date
            buy = sell-timedelta(days=days)
            print "Dividend #%s [%s] = $%s" % (i, date, self.div_data[sell])
            price_yield = (self.tick_data[sell]['Open']-self.tick_data[buy]['Close']) / self.tick_data[buy]['Close']

            # AWV 11/21
            # want smart filter to know that dividend didn't exit back then and return profit for smaller segment.
            pnl = (self.tick_data[sell]['Open'] - self.tick_data[buy]['Close']) + self.div_data[sell]['Dividends']
            sum_pnl += pnl
            print "Yield(price): %s%%, PNL: %s" % (price_yield, pnl)

        print "Thoughts?"
        print "$", sum_pnl


tv = 0.0
start_date = datetime.date(2013,1,1)
# think about coding this as a relative delta
# end_date = datetime.date(2012,1,10)
end_date = datetime.datetime.today()
print start_date, " to ", end_date
#single_stock = raw_input("Input stock? ")
single_stock = False
if single_stock:
    dow = [single_stock]
else:
    dow = ['MRK','DIS','WMT','TRV','KO','HD','MCD','JNJ','MMM','CVX','UTX','MSFT','DD','IBM','PFE','BA','XOM','INTC','AA','CAT','PG','VZ','T','AXP','JPM','CSCO','GE','HPQ','BAC']
print "Stock, Price Yield, Dividend Yield, Total"
transactions = 0

Dow = Stock('^DJI')
Dow.start_date = start_date
Dow.end_date = end_date
Dow.grab_stock_data()
dow_yields = Dow.price_yield('Open')

for stock in dow:
    #print stock
    symbol = stock
    
    mo = Stock(symbol)
    mo.start_date = start_date
    mo.end_date = end_date
    mo.grab_stock_data()
    mo.grab_dividends()
    pyields_open = mo.price_yield('Open')
    dyields = mo.div_yield()
    

    ind_stock = 0
    for i, pyield in enumerate(pyields_open):
        transactions += 1
        rp = round(pyield,6)
        rd = round(dyields[i], 6)
        sumy = rp + rd
        #print "%s,%s,%s,%s" % (stock,rp, rd, sumy)
        ind_stock += sumy
        tv += sumy

    print "buy stock? %s : %s" % (stock,ind_stock)
print "buy port? : %s" % tv
