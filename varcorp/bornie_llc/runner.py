#utils
from utils import *
from stock import Stock
from market import Market




class Runner(object):
    def __init__(self,dow):
        tv = 0.0
        start_date = datetime.date(2013,12,28)
# think about coding this as a relative delta
# end_date = datetime.date(2012,1,10)

        end_date = datetime.date(2014,2,18)
        #print start_date, " to ", end_date

        #single_stock = raw_input("Input stock? ")
#single_stock = False

#hard coded test stock 
        for symbol in dow:
            try:
                mo = Stock(symbol, start_date=start_date, end_date=end_date)
            except Exception, e:
                print "%s failed - %s" % (symbol, e)
