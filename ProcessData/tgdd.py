from ast import Yield
from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

source_database =client['DataIntegration']
source_collections = source_database['tgdd']

target_database =client['ProcessData']
target_collections = target_database['tgdd']

items = source_collections.find({"device":"laptop"})
num_valid_product = 0
num_error_product = 0
error_products = []

for item in items:
    try :
        data =  {
            'product_name ': item['item_name'].replace(u'\xa0', u' '),
            'price': item['price'].replace(u'\xa0', u' ').replace('₫','').replace('.',''),
            'image_url': item['image_url'][0],
            'product_url': item['url'],
            'CPU': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("CPU:") + 1:item['device_detail_infor'].index("RAM:")]),
            'RAM': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("RAM:") + 1:item['device_detail_infor'].index("Ổ cứng:")]),
            'Ổ cứng': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Ổ cứng:") + 1:item['device_detail_infor'].index("Màn hình:")]),
            'Màn hình': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Màn hình:") + 1:item['device_detail_infor'].index("Card màn hình:")]),
            'Card màn hình': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Card màn hình:") + 1:item['device_detail_infor'].index("Cổng kết nối:")]),
            'Hệ điều hành': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Hệ điều hành:") + 1:item['device_detail_infor'].index("Thiết kế:")]),
            'Thiết kế': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Thiết kế:") + 1:item['device_detail_infor'].index("Kích thước, trọng lượng:")]),
            'Thời điểm ra mắt': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Thời điểm ra mắt:") + 1:]),
        }
        try :
            data.update({'Cổng kết nối': " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Cổng kết nối:") + 1:item['device_detail_infor'].index("Đặc biệt:")])})
        except Exception as e:
            data.update({'Cổng kết nối' : " ".join(str(x) for x in item['device_detail_infor'][item['device_detail_infor'].index("Cổng kết nối:") + 1:item['device_detail_infor'].index("Hệ điều hành:")])}),
        print(data)
        target_collections.insert_one(data)
        num_valid_product = num_valid_product + 1
    except ValueError as e:
        print(str(e))
        num_error_product = num_error_product + 1
        error_products.append(item['item-name'])
print (num_valid_product)
print (num_error_product)
print(error_products)