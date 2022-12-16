import html_to_json
import pycurl
import certifi
from io import BytesIO
import argparse
import requests
import time
import json
import vnstock
from common import config

CONF = config.load_config("config.ini")
#top_coin = CONF['Coin']['top']

parser = argparse.ArgumentParser( prog = 'query_data' , 
                                  description= 'to query data on web')

#parser.add_argument('url', help='url of web')
parser.add_argument('-c', help="token to query" )
parser.add_argument('-s', help="stock to query")
parser.add_argument('-t', help="ID to send telegram report ")

time_now = time.ctime()

def list_all_pair(pair):
    # list all symbol with pair 
    url = "https://api.binance.com/api/v3/ticker/bookTicker"
    resp = requests.get(url)
    tickers_list = json.loads(resp.content)
    symbols  = []
    for ticker in tickers_list :
        if str(ticker['symbol'])[-len(pair):] == pair :
            symbols.append(ticker['symbol'])
    return symbols

def query_coin(token):
    key = "https://api.binance.com/api/v3/ticker/price?symbol={}".format(token.upper())
    data = requests.get(key)  
    data = data.json()
    data['Time'] = time_now
    #data["price_{}".format(token)] = data.pop('price')
    #data["price_{}".format(token)] = float(data["price_{}".format(token)])
    data["price"] = float(data["price"])
    data["type"] = "coin"
    data = json.dumps(data)
    ##write it down
    f = open ("/opt/data/data-coin-{}.json".format(token), "w")
    f.write(data)
    f.close
    
    return data


if __name__ == "__main__":
  args = parser.parse_args()

  for i in list_all_pair("USDT")[:100]:
        query_coin(i) 

