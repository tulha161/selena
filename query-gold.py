import html_to_json
import pycurl
import certifi
from io import BytesIO
import argparse
import requests
import time
import json
parser = argparse.ArgumentParser( prog = 'query_data' , 
                                  description= 'to query data on web')

parser.add_argument('url', help='url of web')


time_now = time.ctime()

def query_data(url):
# Creating a buffer as the cURL is not allocating a buffer for the network response
    buffer = BytesIO()
    c = pycurl.Curl()
#initializing the request URL
    c.setopt(c.URL, url)
#setting options for cURL transfer  
    c.setopt(c.WRITEDATA, buffer)
#setting the file name holding the certificates
    c.setopt(c.CAINFO, certifi.where())
# perform file transfer
    c.perform()
#Ending the session and freeing the resources
    c.close()

    body = buffer.getvalue().decode('utf8')
# convert to json:
    body_to_json = html_to_json.convert(body)
    return body_to_json

def query_btc():
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    data = requests.get(key)  
    data = data.json()
    data['Time'] = time_now
    data['price_btc'] = data.pop('price')
    data['price_btc'] = float(data['price_btc'])
    data = json.dumps(data)
    print (data)
    return data



def cut_data_gold():
    data = query_data('https://giavang.org/trong-nuoc/bao-tin-minh-chau/')
    final_data = {}
    cuted = data['html'][0]['body'][0]['main'][0]['div'][0]['article'][0]['div'][4]['table'][0]['tbody'][0]

## lay gia vang  
## BTMC
    tron = cuted['tr'][1]['td']
    tron_name = tron[0]['_value']
    final_data['Time'] = time_now
    final_data["Tron_tron" + "_buy"] = float(tron[1]['_value'])
    final_data["Tron_tron" + "_sell"] = float(tron[2]['_value'])
## Mieng SJC 
    jsc = cuted['tr'][3]['td']
    jsc_name = jsc[0]['_value']
    final_data["Vang_mieng" + "_buy"] = float(jsc[1]['_value'])
    final_data["Vang_mieng" + "_sell"] = float(jsc[2]['_value'])


    final_data = json.dumps(final_data)
    ## write to file
    f = open ("data-gold", "w")
    f.write(final_data)
    f.close
    return final_data



def send_telegram():
   # data_gold = cut_data_gold()
    data_btc = query_btc()

    apiToken = '5767026483:AAEBA1e1EHJg06tEZXdrTKJxhCHvDY9JMeQ'
    chatID = '705864115'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
   #     response = requests.post(apiURL, json={'chat_id': chatID, 'text': data_gold})
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': data_btc})
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
 #   args = parser.parse_args()
    
 #  url = args.url
    cut_data_gold()