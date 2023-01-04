import requests
import time
from common import config
import json

portfolio = config.load_config("/opt/selena/config.ini")['portfolio']
gold_storage = config.load_config("/opt/selena/config.ini")['gold']

apiToken = config.load_config("/opt/selena/config.ini")['telegram']['apiToken']
selena_report_group = config.load_config("/opt/selena/config.ini")['telegram']['selena_report']
time_now = int(time.time())
url = "http://selena.asia:8428"

def query_price(_type,symbol):
    
    query_format = 'selena_price{type="%s",symbol="%s"}' %(_type,symbol) 
    params = { "query" : query_format ,
                "time" : time_now
    } 
    query = url + "/api/v1/query" 
    
    result = requests.get(query,params).json()
    return float(result['data']['result'][0]['value'][1])

def query_gold_price(data):
    query_format = "selena_" + data
    params = { "query" : query_format ,
                "time" : time_now
    } 
    query = url + "/api/v1/query" 
    result = requests.get(query,params).json()
    return float(result['data']['result'][0]['value'][1])

def convert_currency(x):
     return "{:,}VND".format(x)

def calculator():
    result = []
    Tong_gia_tri = {}
    sum_all = 0
    for i in portfolio :
        i_dict = {}
        num = int(portfolio[i])
        price = query_price('stock',i)
        sum = price * num
        i_dict['Stock_name'] = i
        i_dict['Khoi_Luong'] = num
        i_dict['Gia_Hien_Tai'] = convert_currency(price)
        i_dict['Tong_gia_tri'] = convert_currency(sum)
        i_dict['Tong_value'] = sum
        result.append(i_dict)
    
    for j in result:
        sum_all = sum_all + j['Tong_value']
    Tong_gia_tri['Tong_gia_tri_stock']  = convert_currency(sum_all)
    Tong_gia_tri['Gia_vang'] = convert_currency(query_gold_price("Tron_tron_buy")*100000)
    Tong_gia_tri['Tong_gia_tri_gold'] = convert_currency(float(gold_storage['Tron_tron_buy']) * float(query_gold_price("Tron_tron_buy")) * 100000 )
    result.append(Tong_gia_tri)
#gold :
    
    

    return result

def format_report():
    raw = calculator()
    result_str = "Tong Hop Portfolio  cua ban : \n"
    data_str = ""
    result_str += "{:<12}  {:<10}  {:<11}  {:<12}".format("Ma_CP","Khoi_Luong","Gia_Hien_Tai","Tong_Gia_Tri")
    for i in raw[:-1] :
        data_str += "{:<12}  {:<16}  {:<11}  {:<12}\n".format(i['Stock_name'],i["Khoi_Luong"],i["Gia_Hien_Tai"],i["Tong_gia_tri"])
    
    data_str += "{:<12} {:<12}\n".format("TONG_GIA_TRI_STOCK:" , raw[len(raw)-1]['Tong_gia_tri_stock'])
    data_str += "\n{:<12} {:<12}\n".format("GIA_VANG_HIEN_TAI:", raw[len(raw)-1]['Gia_vang'])
    data_str += "{:<12} {:<12}\n".format("TONG_GIA_TRI_GOLD:", raw[len(raw)-1]['Tong_gia_tri_gold'])
    result_str = result_str +"\n" + data_str
    print (result_str)
    return result_str


def send_telegram(chatid,data):
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    
    try:
        response = requests.post(apiURL, json={'chat_id': chatid, 'text': data})
        if response.status_code == 200 :
            print ("gui thanh cong ! ")
    except Exception as e:
        print(e)




if __name__ == "__main__":
    data = format_report()
    send_telegram(selena_report_group,data)
