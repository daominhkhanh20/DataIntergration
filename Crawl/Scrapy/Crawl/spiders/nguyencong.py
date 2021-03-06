from scrapy import Spider, Request
import json
from pymongo import MongoClient
import re
import pandas as pd
import unicodedata

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['ProcessData']

nc_collections = database['nguyen_cong']


# def parse(sent):
#     results = re.findall('>.*?<', sent)
#     final = []
#     for example in results:
#         example = example.replace('\n', "").strip()
#         example = example.replace('\r', "").strip()
#         example = example.replace('>', "").strip()
#         example = example.replace('<', "").strip()
#         if example != "":
#             final.append(example)
#     return final

# def parser_cpu(sent):
#     if 'ghz' not in sent.lower():
#         return sent, None

#     words = sent.lower().strip().split(" ")
#     speed_indexs = []
#     for idx, word in enumerate(words):
#         if 'ghz' in word:
#             speed_indexs.append(idx)

#     if re.search('(\d+?[.x,])+?\d+?$', words[speed_indexs[0] - 1]):
#         speed_indexs.insert(0, speed_indexs[0] - 1)
    
#     try:
#         if words[speed_indexs[0]-2] == 'up' and words[speed_indexs[0]-1] == 'to':
#             speed_indexs.insert(0, speed_indexs[0] - 2)
#     except:
#         pass
    
#     if speed_indexs[0] != 0:
#         return " ".join(words[: speed_indexs[0]]), " ".join(
#             [words[i] for i in range(speed_indexs[0], speed_indexs[-1] + 1, 1)])
#     return " ".join(words[speed_indexs[-1] + 1:]), " ".join(
#         [words[i] for i in range(speed_indexs[0], speed_indexs[-1] + 1, 1)])


def get_data(url):
    data = pd.read_html(url, encoding='utf-8')
    # print(data[0])
    dict_parser = {}
    index = -1
    for idx in range(len(data)):
        if len(data[idx]) > 1:
            index = idx
            break
    if index == -1:
        return dict_parser

    for idx, row in data[index].iterrows():
        # dict_parser[row[0]] = row[1]
        # print(row[0].encode('iso-8859-1').decode('utf8'))
        # dict_parser[unicodedata.normalize('NFKD', row[0])] = unicodedata.normalize('NFKD', row[1])
        try:
            dict_parser[unicodedata.normalize('NFC', unicodedata.normalize('NFKD', row[0]))] = unicodedata.normalize('NFC',unicodedata.normalize('NFKD', row[1]))
        except:
            dict_parser[row[0]] = row[1]

    return dict_parser


class NguyenCong(Spider):
    name = 'nguyencong'
    base_url = 'https://nguyencongpc.vn/laptop?page='
    key_map = {
        'H??? ??i???u h??nh': ['H??? ??i???u h??nh (b???n quy???n) ??i k??m', 'H??? ??i???u h??nh'],
        'RAM': ['RAM', 'B??? nh??? h??? th???ng'],
        'B??? vi x??? l??': ['B??? vi x??? l??', 'CPU', 'CPU:', 'Ch??p x??? l??', 'B??? VXL', 'Ch??p', 'B??? X??? L?? (Xung nh???p c?? b???n/ Turbo)'],
        # 'cpu speed': ['T???c ?????'],
        'VGA': ['Card m??n h??nh', 'VGA', 'Card VGA'],
        'M??n h??nh': ['T??nh n??ng m??n h??nh', 'M??n h??nh'],
        '????? ph??n gi???i m??n': ['????? ph??n gi???i m??n h??nh'],
        '??? c???ng': ['??? c???ng', '??? ????a c???ng', 'SSD', 'HDD'],
        'Kh???i l?????ng': ['Tr???ng l?????ng', 'C??n n???ng'],
        'Xua????t xu????': ['Xua????t xu????'],
        'Ha??ng': ['T??n Ha??ng', 'H??ng s???n xu???t', 'a??ng sa??n xua????t'],
        'Ma??u sa????c': ['Ma??u s????c/ Ch????t li????u', 'Ma??u sa????c'],
        'pin': ['Pin', 'Kie????u Pin']
    }

    def start_requests(self):
        yield Request(url=self.base_url + str(1), callback=self.parse_items)

    def parse_items(self, response):
        # print(response.url)
        current_page = response.xpath('//*[@class="paging"]/a[@class="current"]/text()').get().strip()
        all_pages = response.xpath('//*[@class="paging"]/a/text()').getall()
        all_pages = [example.strip() for example in all_pages]

        list_urls = response.xpath('//*[@class="p-container"]/a/@href').getall()
        for url in list_urls:
            yield response.follow(url=url, callback=self.parse_content)

        if all_pages[-1] != current_page:
            yield Request(url=self.base_url + str(int(current_page) + 1), callback=self.parse_items)

    def parse_content(self, response):
        price = response.xpath('//*[@class="detail-price"]/span/text()').getall()
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

        image_url = response.xpath("//*[@class='item-n active']/a/img/@src").get()

        data = {
            'device': 'laptop',
            'product_name': response.xpath('//*[@class="header-product-detail"]/h1/text()').get(),
            'price': product_price,
            'product_url': response.url,
            'image_url': f"https://nguyencongpc.vn{image_url}",
        }
        dict_parser = get_data(url=response.url)

        # print(dict_parser)
        if len(dict_parser) == 0:
            return None

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

        nc_collections.insert_one(data)
