from scrapy import Spider, Request
import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

cellphones_collections = database['cellphones']


class CellPhoneS(Spider):
    name = 'cellphones'
    list_phone_url = json.load(open('../Url/cellphones/remain_phone.json', 'r'))
    list_laptop_url = json.load(open('../Url/cellphones/remain_laptop.json', 'r'))
    # list_phone_url_copy = list_phone_url.copy()
    # list_laptop_url_copy = list_laptop_url.copy()

    def start_requests(self):
        if len(self.list_laptop_url) > 0:
            for url in self.list_phone_url:
                yield Request(url=url, callback=self.parse, meta={'device': 'phone'})

        if len(self.list_laptop_url):
            for url in self.list_laptop_url:
                yield Request(url=url, callback=self.parse, meta={'device': 'laptop'})

        # self.save_json('Url/cellphones/remain_phone.json', self.list_phone_url_copy)
        # self.save_json('Url/cellphones/remain_laptop.json', self.list_laptop_url_copy)

    def parse(self, response, **kwargs):
        data = {
            'device': response.meta.get('device', None),
            'url': response.url,
            'image_url': response.xpath('//*[@id="product-mob-images"]/div/img/@data-src').getall(),
            'item_name': response.xpath('//*[@class="box-name__box-product-name"]/h1/text()').get(),
            'price': response.xpath('//*[@class="box-info__box-price"]/p/text()').get(),
            'infor_product': response.xpath('//*[@class="item-warranty-info"]/p/text()').getall(),
            'device_detail_infor': response.xpath("//*[@id='tskt']/tbody/tr/th/text()").getall(),
            'more_offer': response.xpath('//*[@class="item-promotion"]/a/text()').getall(),
            'salient characteristic': response.xpath('//*[@style="text-align: justify;"]/text()').getall()
        }
        cellphones_collections.insert_one(data)
        # if response.meta.get('device', None) == 'phone':
        #     self.list_phone_url_copy.remove(response.url)
        #
        # elif response.meta.get('device', None) == 'laptop':
        #     self.list_laptop_url_copy.remove(response.url)

    def save_json(self, path: str, data: list):
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
