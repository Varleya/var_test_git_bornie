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
    dow = ['MRK','DIS','WMT','TRV','KO','HD','MCD','JNJ','MMM','CVX','UTX','MSFT','DD','IBM','PFE','BA','XOM','INTC','AA','CAT','PG','VZ','T','AXP','JPM','CSCO','GE','HPQ','BAC']
    
    db = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="",
                         db="varcorp")
    cursor = db.cursor()
    cursor.execute("use varcorp")
    
    div_query = "select divdate, amount from %s_dividends where year(divdate) = '2012'"
    tick_query = "select * from %s_ticker"
    market_query = "select * from dow"
    
    # parameters to pass in as options
    buy_delta = timedelta(days=1)
    sell_delta = timedelta(days=0)
    buy_time = 'close'
    sell_time = 'open'
    dumsum = 0
    cursor.execute(market_query)
    dow = dicttick(cursor)

    for symbol in dow:
        cursor.execute((div_query % symbol))
        divs = dictdividends(cursor)
        cursor.execute((tick_query % symbol))
        ticks = dicttick(cursor)
        
        for date, amount in sorted(divs.iteritems()):
            buy_date = validbuydate(date, buy_delta, ticks)
            if not buy_date:
                print "can't get data for %s on %s" % (symbol, date)
                continue
            buy_price = ticks.get(buy_date)[buy_time]
            sell_price = ticks.get(date+sell_delta)[sell_time]
            price_yield = sell_price / buy_price - 1
            div_yield = amount / buy_price
            total_yield = price_yield + div_yield
            print symbol, date, buy_price, sell_price, amount, price_yield, div_yield, total_yield

            dumsum += total_yield
    print dumsum
