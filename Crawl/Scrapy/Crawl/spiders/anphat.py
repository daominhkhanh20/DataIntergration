from scrapy import Spider, Request
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

ap_collections = database['anphat']

class AnPhat(Spider):
    name = 'anphat'

    def start_requests(self):
        # device = getattr(self, 'device', None)
        urls = 'https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html?page={}'

        for page in range(1,19):
            yield Request(url=urls.format(page), callback=self.parse)
   
        
    def parse(self, response):
        base_url = 'https://www.anphatpc.com.vn{}'
        list_url =  response.xpath('//div[@class="p-item "]/a/@href').getall()
        if len(list_url):
            for detail_url in list_url:
                detail_url = base_url.format(detail_url)
                if detail_url is not None:
                    item = {
                        'device':'laptop',
                        'url': detail_url,
                    }

                    yield Request(response.urljoin(detail_url), callback=self.parse_content ,meta={'item': item})


    def parse_content(self, response):
        item = response.meta['item']
        item['image_url'] = response.xpath('//span[@class="img"]/img[@class="fit-img"]/@src').get()
        item['item_name'] = response.xpath('//h1[@class="pro-name js-product-name"]/text()').get()
        item['price'] = response.xpath('//b[@class="text-18 js-pro-total-price"]/@data-price').get()
        item['device_detail_infor'] = response.xpath('//tbody/tr/td/p/span/strong//text()').getall()

        ap_collections.insert_one(item)
        # return item