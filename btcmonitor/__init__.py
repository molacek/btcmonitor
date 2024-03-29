import os
import json
import time
from . import coinbase
from . import svg
from xdg import XDG_CACHE_HOME


def data_interval(data, t):
    min_time = int(time.time()) - t
    return([[t, v] for [t, v] in data if t > min_time])


def main():

    (status, result) = coinbase.get_btc_price()
    if not status:
        if result == coinbase.OFFLINE:
            print("<txt><span fgcolor='Gray'>Offline</span></txt>")
        elif result == coinbase.SERVER_ERROR:
            print("<txt><span fgcolor='Gray'>Server error</span></txt>")
        elif result == coinbase.PARSE_ERROR:
            print("<txt><span fgcolor='Gray'>Parse error</span></txt>")
        else:
            print("<txt><span fgcolor='Gray'>Unknown error</span></txt>")
        return

    btc_price = result

    history_file = XDG_CACHE_HOME / 'btc_price_history.json'
    if os.path.isfile(history_file):
        with open(history_file, 'r') as f:
            btc_price_history = data_interval(json.loads(f.read()), 24*60*60)
    else:
        btc_price_history = []

    if len(btc_price_history) > 1:
        svg.btc_graph(btc_price_history)

    sum_price = 0
    records = 0
    high_price = None
    low_price = None
    actual_ts = int(time.time())
    for ts, price in btc_price_history:
        sum_price += price
        records += 1
        if not high_price:
            high_price = price
        elif price > high_price:
            high_price = price
        if not low_price:
            low_price = price
        elif price < low_price:
            low_price = price

    btc_price_history.append((actual_ts, btc_price))

    with open(history_file, "w") as f:
        f.write(json.dumps(btc_price_history))

    if records > 0:
        btc_average = int(sum_price / records)
    else:
        btc_average = 0

    if btc_average <= btc_price:
        fgcolor = "Green"
    else:
        fgcolor = "#b30000"

    print("<click>xdg-open \"https://cryptowat.ch/"
          "markets/coinbase-pro/btc/usd\"</click>")
    print("<txt><span fgcolor='{0:s}'> {1:d} </span>"
          "</txt>".format(fgcolor, btc_price))
    print("<img>{0:s}</img>".format(
        str(XDG_CACHE_HOME / "btc_graph.svg")))
    if high_price is not None:
        print("<tool>AVG: {0:d}\nHigh: {1:d}\nLow: {2:d}"
              "</tool>".format(btc_average, high_price, low_price))
