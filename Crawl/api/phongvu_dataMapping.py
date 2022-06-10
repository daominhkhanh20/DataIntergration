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

pv_collections = database['phongvu_mapping']

list_laptop_url = json.load(open('../Url/phongvu/phongvu_laptop_url.json', 'r'))

def convert(list_url):
    list_product_id = []
    for dict_url in list_url:
        id = dict_url['url'].split('=')[-1]
        list_product_id.append([int(id),dict_url['url']])
    return list_product_id

def getProductDetail(list_product_id,topic):
    url_detail_item = 'https://phongvu.vn/api/product/{}'
    for x in tqdm(range(len(list_product_id))):
        time.sleep(0.3)
        id = list_product_id[x][0]
        try:
            data = requests.get(url_detail_item.format(id)).content
            data = json.loads(data)

            def recursive_items(dictionary):
                if type(dictionary) is dict:
                    for key, value in dictionary.items():
                        if type(value) is dict:
                            yield from recursive_items(value)
                        elif type(value) is list:
                            for sub_value in value:
                                yield from recursive_items(sub_value)
                        else:
                            yield (key, value)

            dict_result = {}
            dict_result['define_project_id'] = x
            dict_unique = {}
            for key, value in recursive_items(data):
                if key not in dict_unique.keys():
                    dict_unique[key] = 0
                    dict_result[key] = value
                else:
                    dict_unique[key] += 1
                    dict_result[f'{key}_{dict_unique[key]}'] = value

            pv_collections.insert_one(dict_result)
        except Exception as e:
            print(e)



list_laptop_url = convert(list_laptop_url)

laptop_pd = getProductDetail(list_laptop_url,'laptop')