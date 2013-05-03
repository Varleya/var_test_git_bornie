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
