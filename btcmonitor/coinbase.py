import requests
import os
import sys
import time
import json

OK = 0
OFFLINE = 1
SERVER_ERROR = 2
PARSE_ERROR = 3

def get_btc_price():
    url = "https://api.pro.coinbase.com/products/btc-usd/ticker"

    try:
        response = requests.request("GET", url)
    except:
        return(False, OFFLINE )

    if response.status_code >= 500:
        return(False, SERVER_ERROR )

    try:
        btc_stats = response.json()
        btc_price = int(btc_stats["price"].split('.')[0])
    except:
        return(False, PARSE_ERROR)

    return(True, btc_price)
