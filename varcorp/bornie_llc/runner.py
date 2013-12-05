#utils
from utils import *
from stock import Stock
from market import Market

tv = 0.0
start_date = datetime.date(2013,1,1)
# think about coding this as a relative delta
# end_date = datetime.date(2012,1,10)

end_date = datetime.date(2013,12,1)
print start_date, " to ", end_date

single_stock = raw_input("Input stock? ")
#single_stock = False
if single_stock:
    dow = [single_stock]
else:
    #dow = ['TK', 'GPS', 'STEI']
   # dow = ['AIG','FDUS','FDUS','FISI','GARS','GCAP','GK','LMOS','MCY','MDU','MPW','MRVL','SFL']
    dow = ['MRK','DIS','WMT','TRV','KO','HD','MCD','JNJ','MMM','CVX','UTX','MSFT','DD','IBM','PFE','BA','XOM','INTC','AA','CAT','PG','VZ','T','AXP','JPM','CSCO','GE','BAC', 'SPY']
    #dow = ['T]
#    dow = ['T', 'VZ', 'INTC', 'MRK', 'MCD', 'CVX', 'MSFT', 'PFE', 'PG', 'DD']

#hard coded test stock 
for symbol in dow:

    mo = Stock(symbol, start_date=start_date, end_date=end_date)
    mo.start_date = start_date
    mo.end_date = end_date
