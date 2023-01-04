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
parser.add_argument('-p', help="Chi dinh cap pair ")

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
    data["price"] = float(data["price"])
    data["type"] = "coin"
    data = json.dumps(data)
    ##write it down
    #f = open ("/opt/data//data-coin-{}".format(token), "w")
    #f.write(data)
    #f.close
    
    return data
def query_list_coin(pair):
    all_data = []
    for i in list_all_pair(pair) :
        print (i)
        data = query_coin(i)
        all_data.append(data)
    all_data = json.dumps(all_data)
    f = open ("/opt/test_dr/data-all-coin", "w")
    f.write(all_data)
    f.close


def query_stock(stock):
    data = vnstock.price_board(stock).get("Giá Khớp Lệnh").to_json()
    to_dict = json.loads(data)
    #to_dict["stock_{}".format(stock)] = to_dict.pop("0")
    if to_dict['0'] is not None :
        to_dict["price"] = to_dict.pop("0")
        to_dict["symbol"] = stock
        to_dict["Time"] = time_now
        to_dict["type"] = "stock"
        f_data = json.dumps(to_dict)
        f = open ("/opt/data/data-stock-{}".format(stock), "w")
        f.write(f_data)
        f.close
        return f_data
    else : 
        print ("None data, not collect anything")



def send_telegram(data,t):
   # data_gold = cut_data_gold()
    

    apiToken = '5767026483:AAEBA1e1EHJg06tEZXdrTKJxhCHvDY9JMeQ'
    chatID = t
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
   #     response = requests.post(apiURL, json={'chat_id': chatID, 'text': data_gold})
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': data})

    except Exception as e:
        print(e)
    #data["price_{}".format(token)] = data.pop('price')
    #data["price_{}".format(token)] = float(data["price_{}".format(token)])

if __name__ == "__main__":
  args = parser.parse_args()
 #  url = args.url
  if args.c :
    token = args.c
    data = query_coin(token)
    if args.c and args.t :
        send_telegram(data,args.t)
  if args.s : 
    data = query_stock(args.s)
    if args.s and args.t :
        send_telegram(data,args.t)

  if args.p :
    query_list_coin(args.p)
