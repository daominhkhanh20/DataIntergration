from ast import Yield
import os
from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database =client['ProcessData']
pa_collections = database['phucanh']


class Phucanh(Spider):
        name = 'phucanhprocess'
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
                            'product_url': detail_url
                        }

                        #yield item
                        yield Request(response.urljoin(detail_url), callback=self.parse_content ,meta={'item': item})
                        
        def getData(self,item):
            data = pd.read_html(item['product_url'],encoding='utf8')
            for item in data:
                if item.shape[0] > 15:
                    data = item
                    break
            
            

            
            
            dict_loader = {}
            iter = 0
            for id, item in data.iterrows():
                if item[0] in dict_loader.keys():
                    iter +=1
                    dict_loader[f'{item[0]}_{iter}'] = item[1]
                else:
                    dict_loader[item[0]] = item[1]
            return dict_loader
        def parse_content(self, response):
            item = response.meta['item']
            item ['product_name'] =  response.xpath('//div[@class="container"]/h1/text()').get()
            item['price'] = response.xpath('//span[@class="detail-product-best-price"]/text()').get()
            item['image_url']= response.xpath('//div[@class="item"]/a/img/@src').get()
            item.update(self.getData(item))         

            #return item
            pa_collections.insert_one(item)
            #yield item

            



