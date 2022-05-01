from scrapy import Spider, Request
import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

cellphones_collections = database['cellphones']


class CellPhoneS(Spider):
    name = 'cellphones'
    list_phone_url = json.load(open('Url/cellphones/final_phone.json', 'r'))
    list_laptop_url = []
    #list_laptop_url = json.load(open('Url/cellphones/laptop.json', 'r'))

    def start_requests(self):
        for url in self.list_phone_url + self.list_laptop_url:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        data = {
            'item_name': response.xpath('//*[@class="box-name__box-product-name"]/h1/text()').get(),
            'price': response.xpath('//*[@class="box-info__box-price"]/p/text()').get(),
            'infor_product': response.xpath('//*[@class="item-warranty-info"]/p/text()').getall(),
            'device_detail_infor': response.xpath("//*[@id='tskt']/tbody/tr/th/text()").getall(),
            'more_offer': response.xpath('//*[@class="item-promotion"]/a/text()').getall(),
            'salient characteristic': response.xpath('//*[@style="text-align: justify;"]/text()').getall()
        }
        cellphones_collections.insert_one(data)
