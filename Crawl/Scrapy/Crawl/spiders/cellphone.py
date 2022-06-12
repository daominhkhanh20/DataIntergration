from scrapy import Spider, Request
import json
from pymongo import MongoClient
import pandas as pd
import unicodedata
import re

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['ProcessData']

cellphones_collections = database['cellphones']


# def parser_cpu(sent):
#     if 'ghz' not in sent.lower():
#         return sent, None
#
#     words = sent.lower().split(" ")
#     speed_indexs = []
#     for idx, word in enumerate(words):
#         if 'ghz' in word:
#             speed_indexs.append(idx)
#
#     if re.match('(\d+?[.x,])+?\d+?$', words[speed_indexs[0] - 1]):
#         speed_indexs.insert(0, speed_indexs[0] - 1)
#
#     if speed_indexs[0] != 0:
#         return " ".join(words[: speed_indexs[0]]), " ".join(
#             [words[i] for i in range(speed_indexs[0], speed_indexs[-1] + 1, 1)])
#     return " ".join(words[speed_indexs[-1] + 1:]), " ".join(
#         [words[i] for i in range(speed_indexs[0], speed_indexs[-1] + 1, 1)])


def get_result(url, debug_mode: bool = False):
    data = pd.read_html(url)
    if debug_mode:
        print(data)
        print(data[0].to_dict())
    sample = list(data[0].to_dict().keys())
    if not isinstance(sample[0], tuple):
        sample = list(data[1].to_dict().keys())
    pair = {}
    for i in range(len(sample[0])):
        pair[sample[0][i]] = sample[1][i]

    return pair


class CellPhoneS(Spider):
    name = 'cellphones'
    list_phone_url = json.load(open('../Url/cellphones/final_phone.json', 'r'))
    list_laptop_url = json.load(open('../Url/cellphones/final_laptop.json', 'r'))
    key_map = {
        'Hệ điều hành': ['Hệ điều hành'],
        'ram': ['Dung lượng RAM'],
        'Loại CPU': ['Loại CPU', 'Chipset'],
        'gpu': ['Loại card đồ họa'],
        'màn hình': ['Tính năng màn hình', 'Công nghệ màn hình', 'Kích thước màn hình'],
        'Độ phân giải màn ': ['Độ phân giải màn hình'],
        'Ổ cứng': ['Ổ cứng', 'Bộ nhớ trong'],
        'Trọng lượng': ['Trọng lượng'],
        'pin': ['Pin']
    }

    def start_requests(self):
        self.device = getattr(self, 'device', None)
        if self.device == 'phone':
            for url in self.list_phone_url:
                yield Request(url=url, callback=self.parse, meta={'device': 'phone'})
        elif self.device == 'laptop':
            for url in self.list_laptop_url:
                yield Request(url=url, callback=self.parse, meta={'device': 'laptop'})

    def parse(self, response, **kwargs):
        price = response.xpath('//*[@class="box-info__box-price"]/p/text()').getall()
        if len(price) == 0:
            return None
        else:
            if len(price) == 1:
                product_price = price[0]
            else:
                product_price = -1
                for term in price:
                    if any(char.isdigit() for char in term):
                        product_price = unicodedata.normalize('NFKD', term)
                        break
        if product_price == -1:
            return None

        data = {
            'device': response.meta.get('device', None),
            'product_name': response.xpath('//*[@class="box-name__box-product-name"]/h1/text()').get().strip(),
            'price': product_price,
            'image_url': response.xpath('//*[@id="product-mob-images"]/div/img/@data-src').get(),
            'product_url': response.url,
        }
        dict_parser = get_result(url=response.url)

        list_keys = list(dict_parser.keys())
        list_keys_added = []
        for attribute in self.key_map.keys():
            if self.key_map[attribute] is not None:
                for name in self.key_map[attribute]:
                    name_key = None
                    for key in list_keys:
                        if name.lower() in key.lower():
                            name_key = key
                    if name_key is None:
                        continue
                    temp = dict_parser.get(name_key, None)
                    data[attribute] = temp
                    list_keys_added.append(name_key)
                    break
        if len(data.keys()) == 5:
            return None

        list_key_remains = list(set(list_keys) ^ set(list_keys_added))
        for key in list_key_remains:
            data[key] = dict_parser[key]

        cellphones_collections.insert_one(data)

    # def parse(self, response, **kwargs):
    #     data = {
    #         'device': response.meta.get('device', None),
    #         'url': response.url,
    #         'image_url': response.xpath('//*[@id="product-mob-images"]/div/img/@data-src').getall(),
    #         'item_name': response.xpath('//*[@class="box-name__box-product-name"]/h1/text()').get(),
    #         'price': response.xpath('//*[@class="box-info__box-price"]/p/text()').get(),
    #         'infor_product': response.xpath('//*[@class="item-warranty-info"]/p/text()').getall(),
    #         'device_detail_infor': response.xpath("//*[@id='tskt']/tbody/tr/th/text()").getall(),
    #         'more_offer': response.xpath('//*[@class="item-promotion"]/a/text()').getall(),
    #         'salient characteristic': response.xpath('//*[@style="text-align: justify;"]/text()').getall()
    #     }
    #     # cellphones_collections.insert_one(data)
    #     # if response.meta.get('device', None) == 'phone':
    #     #     self.list_phone_url_copy.remove(response.url)
    #     #
    #     # elif response.meta.get('device', None) == 'laptop':
    #     #     self.list_laptop_url_copy.remove(response.url)
    #
    # def save_json(self, path: str, data: list):
    #     with open(path, 'w') as file:
    #         json.dump(data, file, indent=4)
