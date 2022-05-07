from scrapy import Spider, Request
import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

tgdd_collections = database['tgdd']


class Tgdd(Spider):
    name = 'tgdd'
    list_phone_url = json.load(open('Url/tgdd/phone.json', 'r'))
    list_laptop_url = json.load(open('Url/tgdd/laptop.json', 'r'))

    def start_requests(self):
        for url in self.list_phone_url:
            yield Request(url=url, callback=self.parse, meta={'device': 'phone'})

        for url in self.list_laptop_url:
            yield Request(url=url, callback=self.parse, meta={'device': 'laptop'})


    def parse(self, response, **kwargs):
        data = {
            'device': response.meta.get('device', None),
            'url': response.url,
            'image_url': response.xpath('//div[@class="item-border"]/img/@data-src').getall(),
            'item_name': response.xpath('//section[@class="detail "]/h1/text()').get(),
            'price': response.xpath('//div[@class="box-price"]/p/text()').get(),
            'infor_product': [text.strip() for text in response.xpath('//div/ul[@class="policy__list"]/li/p').css('*:not(style)::text').extract() if text.strip()],
            'device_detail_infor': [text.strip() for text in response.xpath('//div[@class="parameter"]/ul/li').css('*:not(style)::text').extract() if text.strip()],
            'more_offer': response.xpath('//div[@class="promoadd "]/ul/li/p/text()').getall(),
            'salient characteristic': [text.strip() for text in response.xpath('//div[@class="content-article"]/p').css('*:not(style)::text').extract() if text.strip()]
        }
        print(data)
        tgdd_collections.insert_one(data)

