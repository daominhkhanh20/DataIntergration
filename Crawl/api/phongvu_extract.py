import json
import requests 
import json
import pandas as pd
from tqdm import tqdm
import pickle
import time


from pymongo import MongoClient
client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

pv_collections = database['phongvu']

list_laptop_url = json.load(open('../Url/phongvu/phongvu_laptop_url.json', 'r'))
list_phone_url = json.load(open('../Url/phongvu/phongvu_phone_url.json', 'r'))

def convert(list_url):
    list_product_id = []
    for dict_url in list_url:
        id = dict_url['url'].split('=')[-1]
        list_product_id.append([int(id),dict_url['url']])
    return list_product_id

def getProductDetail(list_product_id,topic):
    url_detail_item = 'https://phongvu.vn/api/product/{}'
    df = []
    for x in tqdm(range(len(list_product_id))):
        time.sleep(0.3)
        id = list_product_id[x][0]
        try:
            item = {}
            data = requests.get(url_detail_item.format(id)).content
            data = json.loads(data)['result']['product']
            

            item['device'] = str(topic)
            item['url'] = list_product_id[x][1]
            item['image_url'] = data['productInfo']['imageUrl']
            item['item_name'] = data['productInfo']['name']
            item['brand'] = data['productInfo']['brand']['code']
            item['prices'] = int(data['prices'][0]['latestPrice'])
            item['id'] = list_product_id[x][1]
            device_detail_infor = []
            for attb in data['productDetail']['attributeGroups']:
                device_detail_infor.append({attb['name']:attb['value']})
            item['device_detail_infor'] = device_detail_infor
            
            df.append(item)
        except:
            print('Crawl website error')
    return df


list_laptop_url = convert(list_laptop_url)
list_phone_url = convert(list_phone_url)

laptop_pd = getProductDetail(list_laptop_url,'laptop')
phone_pd = getProductDetail(list_phone_url,'phone')
pv_collections.insert_many(laptop_pd)
pv_collections.insert_many(phone_pd)


