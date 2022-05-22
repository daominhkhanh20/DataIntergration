from ast import Yield
from scrapy import Spider, Request
from pymongo import MongoClient

client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database =client['DataIntegration']
pa_collections = database['phucanh']


class Phucanh(Spider):
        name = 'phucanh'
        base_url = 'https://www.phucanh.vn/{}'


        def start_requests(self):
            device = 'laptop'

            urls = 'https://www.phucanh.vn/laptop.html?page={}'
            for page in range(1,21):
                yield Request(url=urls.format(page), callback=self.parse)
                
        

        def parse(self, response):
            base_url = 'https://www.phucanh.vn/{}'
            list_url = response.xpath('//div[@class="p-container"]/a[@class="p-img"]/@href').getall()

            if len(list_url):
                for detail_url in list_url:
                    detail_url = base_url.format(detail_url)
                    if detail_url is not None:
                        item = {
                            'device': 'laptop',
                            'url': detail_url
                        }

                        #yield item

                        request = Request(response.urljoin(detail_url), callback=self.parse_content)
                        request.meta['item'] = item
                        yield request
                        
        
        def parse_content(self, response):
            item = response.meta['item']
            item['image_url']= response.xpath('//div[@class="item"]/a/img/@src').getall()
            item ['item-name'] =  response.xpath('//div[@class="container"]/h1/text()').get()
            item['price'] = response.xpath('//span[@class="detail-product-best-price"]/text()').get()
            item['device_detail_info'] =   response.xpath('//div[@class="tbl-technical nd"]/table/tbody/tr/td/text()').getall()
            

            #return item
            pa_collections.insert_one(item)
            # yield item

            



