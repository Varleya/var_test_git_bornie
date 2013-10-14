import urllib
import MySQLdb
import csv
from datetime import timedelta
def dictdividends(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    divdict = {}
    for date, amount in cursor.fetchall():
        divdict[date] = amount
    return divdict
#    return [
#        dict(zip([col[0] for col in desc], row))
#        for row in cursor.fetchall()]


def dicttick(cursor):
    desc = cursor.description
    tickdict = {}
    try:
        for db_row in cursor.fetchall():
            tickdict[db_row[1]] = {}
            for i, col in enumerate(db_row[2:]):
                tickdict[db_row[1]][desc[i+2][0]]= col
    except Exception, e:
        import debug
    return tickdict

def dicttick(cursor):
    desc = cursor.description
    tickdict = {}
    try:
        for db_row in cursor.fetchall():
            tickdict[db_row[1]] = {}
            for i, col in enumerate(db_row[2:]):
                tickdict[db_row[1]][desc[i+2][0]]= col
    except Exception, e:
        import debug
    return tickdict


def validbuydate(date, buy_delta, data):
    count = 5
    while count > 0:
        try:
            data[date-buy_delta]
            return date-buy_delta
        except:
            buy_delta = buy_delta + timedelta(days=1)
            count -= 1
    return None





if __name__ == '__main__':
	# will want this to be filled with options
    port = ['MRK','DIS','WMT','TRV','KO','HD','MCD','JNJ','MMM','CVX','UTX','MSFT','DD','IBM','PFE','BA','XOM','INTC','AA','CAT','PG','VZ','T','AXP','JPM','CSCO','GE','HPQ','BAC','SPY']
    #port = ['GPS', 'TK', 'STEI']    
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="varcorp")
    cursor = db.cursor()
    cursor.execute("use varcorp")
    
    div_query = "select divdate, amount from %s_dividends where year(divdate) = '2013' or year(divdate)='2012'"
    tick_query = "select * from %s_ticker where year(tickdate) = '2008' or year(tickdate)='2007' or  year(tickdate)='2009'"
    market_query = "select * from SPY_ticker"
    
    # parameters to pass in as options
    buy_delta = timedelta(days=1)
    sell_delta = timedelta(days=0)
    buy_time = 'close'
    sell_time = 'open'
    dumsum = 0.0

    #prep market data
    cursor.execute(market_query)
    market = dicttick(cursor)
    market_dumsum = 0.0 


    openp = 3
    closep = 6
    low = 5 
    
    print "symbol, date, buy_price, sell_price, amount, price_yield, div_yield, total_yield"
    for symbol in port:
        market_time = 0.0 
        over_time = 0.0
        
        cursor.execute((tick_query % symbol))
        headers =  map(lambda x: x[0], cursor.description)
       # ticks = dicttick(cursor)
        
        totals = 0.0
        buy_price = None
        buys = 0 
        for data in sorted(cursor.fetchall()):
            # if bought, figure out won/loss
            price_change = data[closep]-data[openp]
            if buy_price:
                realized_1day = data[closep] / buy_price - 1
                totals += realized_1day

            
            #stock went up in a day
            if price_change > 0:
                buy_price = None
                pass
            else:
                buys += 1
                buy_price = data[closep]
        if symbol != 'SPY':
            dumsum += totals

        print ",".join(str(d) for d in [symbol, totals,buys])
    print dumsum
    #print ",".join(str(d) for d in [symbol, date, buy_price, sell_price, amount, price_yield, div_yield, total_yield, market_yield])
