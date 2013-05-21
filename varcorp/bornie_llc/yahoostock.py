
import urllib2
from urllib import urlencode
from utils import *
import MySQLdb
import csv


class YahooDividend(object):
    def __init__(self, ticker, **args):
        if not ticker:
            raise Exception, "must supply stock symbol"
        self.ticker = ticker
        self.qurl = "http://ichart.yahoo.com/table.csv?s=" + ticker
        self.start_date = args.get('start_date')
        self.end_date = args.get('end_date')
        self.data = {}


    def save_data(self,data):
        db = MySQLdb.connect(host="localhost",
                             user="root",
                             passwd="",
                             db="varcorp")
        
        #check if table exists
        cursor = db.cursor()
        create_table = "CREATE TABLE {0}_dividends (divdate DATE not NULL, amount FLOAT(6,6))".format(self.ticker)

        try:
            cursor.execute("select * from {0}_dividends limit 1".format(self.ticker))
            cursor.execute("drop table {0}_dividends".format(self.ticker))
        except:
            print "first time"
            pass
        cursor.execute(create_table)
        # insert existing CSV into SQL
        insert_sql = """
        LOAD DATA LOCAL INFILE '{0}_dividends.csv' 
        INTO TABLE {0}_dividends FIELDS TERMINATED BY ',' 
        IGNORE 1 LINES;
        """.format(self.ticker)

        # enter data and commit to DB
        cursor.execute(insert_sql)
        db.commit()
        db.close()


    def grab_data(self):
        # this later can be smarter about where data comes from
        if self.start_date is None or self.end_date is None:
            raise Exception, "Missing Dates"

        url = "%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s&g=v&ignore=.csv" % \
            (self.qurl, (self.start_date.month-1), self.start_date.day, self.start_date.year \
            ,(self.end_date.month-1), self.end_date.day, self.end_date.year)
        
        #actually grab data and grab as text
        pdata = urllib2.urlopen(url)
        rows = pdata.readlines()

        with open('{0}_dividends.csv'.format(self.ticker) , 'wb') as f:
            writer = csv.writer(f, delimiter=',')
            for row in rows:
                data = [r.strip() for r in row.split(',')]
                writer.writerow(data)
        
        self.save_data(rows[1:])
        # first row comes back with header, so to store just return everything after that
        pdata.close()
