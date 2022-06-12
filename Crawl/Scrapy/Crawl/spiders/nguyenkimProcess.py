from ast import Yield
import imp
from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd
client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database =client['ProcessData']
nk_collections = database['nguyenkim']


class Nguyenkim(Spider):
        name = 'nguyenkimprocess'
        base_url = 'https://www.nguyenkim.com/{}'


        def start_requests(self):
            device = 'phone'

            urls = 'https://www.nguyenkim.com/may-tinh-xach-tay/page-{}/'
            for page in range(1,6):
                yield Request(url=urls.format(page), callback=self.parse)
                
        

        def parse(self, response):
            
            list_url = response.xpath('//div[@class="item-list product"]/div[@class="product-header"]/div[@class="product-image"]/a/@href').getall()

            if len(list_url):
                for url in list_url:
                    #detail_url = base_url.format(detail_url)
                    if url is not None:
                        item = {
                            'device': 'laptop',
                            'product_url': url
                        }

                        #yield item

                        yield Request(response.urljoin(url), callback=self.parse_content ,meta={'item': item})
                        
        def getData(self,item):
            data= pd.read_html(item['product_url'],encoding='utf8')
            for item in data:
                if item.shape[0] > 15:
                    data = item
                    break
            
            dict_loader = {}
            iter = 0 
            for id,item in data.iterrows():
                if item[0] in dict_loader.keys():
                    iter += 1
                    dict_loader[f'{item[0]}_{iter}'] = item[1]
                else:
                    dict_loader[item[0]] = item[1]
            return dict_loader

        def parse_content(self, response):
            item = response.meta['item']
            item ['product_name'] =  response.xpath('//div[@class="wrap_name_vote"]/h1[@class="product_info_name"]/text()').get()
            item['price'] = response.xpath('//div[@class="product_info_price_value-final"]/span/text()').get()
            item['image_url']=  response.xpath('//div[@class="wrap-img-tag-pdp"]/img/@src').get()
            item.update(self.getData(item))
            

            #return item
            nk_collections.insert_one(item)
            # yield item

            



