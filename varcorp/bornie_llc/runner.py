#utils
from utils import *
from stock import Stock
from market import Market


tv = 0.0
start_date = datetime.date(2000,1,1)
# think about coding this as a relative delta
# end_date = datetime.date(2012,1,10)

end_date = datetime.date(2013,5,1)
print start_date, " to ", end_date

#single_stock = raw_input("Input stock? ")
single_stock = False
if single_stock:
    dow = [single_stock]
else:
    dow = ['MRK','DIS','WMT','TRV','KO','HD','MCD','JNJ','MMM','CVX','UTX','MSFT','DD','IBM','PFE','BA','XOM','INTC','AA','CAT','PG','VZ','T','AXP','JPM','CSCO','GE','HPQ','BAC']
print "Stock, Price Yield, Dividend Yield, Total"

#hard coded test stock 

dow = ["GE"]

for stock in dow:
    #print stock
    symbol = stock

    mo = Stock(symbol, start_date=start_date, end_date=end_date)
    mo.start_date = start_date
    mo.end_date = end_date
    # mo.grab_stock_data()
    # mo.grab_dividends()
    #give relevant dates to Market class
#     market.grab_dividends(mo.div_dates)

#     pyields_open = mo.price_yield('Open')
#     dyields = mo.div_yield()
#     market_yields = market.price_yield('Open')
#     ind_stock = 0

#     for i, pyield in enumerate(pyields_open):
#         transactions += 1
#         rp = round(pyield,6)
#         rd = round(dyields[i], 6)
#         sumy = rp + rd
        
#         #print "%s,%s,%s,%s" % (stock,rp, rd, sumy)
#         ind_stock += sumy
#         tv += sumy

#     print "buy stock? %s : %s" % (stock,ind_stock,sum(market_yields))
#     tmv += sum(market_yields)

# print "buy port? : %s -- > market : %s" % (tv, tmv)
