from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['ProcessData']

hnncmp_collections = database['hanoicmp']

class AnPhat(Spider):
    name = 'hanoicmp'

    def start_requests(self):
        # device = getattr(self, 'device', None)
        urls = 'https://hacom.vn/laptop-tablet-mobile/{}/'

        for page in range(1,12):
            yield Request(url=urls.format(page), callback=self.parse)
   
        
    def parse(self, response):
        base_url = 'https://hacom.vn{}'
        list_url =  response.xpath('//div[2]/a/@href').getall()
        if len(list_url):
            for detail_url in list_url:
                if 'laptop' in detail_url and 'laptop-tablet' not in detail_url:
                    detail_url = base_url.format(detail_url)
                    if detail_url is not None:
                        item = {
                            'device':'laptop',
                            'product_url': detail_url,
                        }

                        yield Request(response.urljoin(detail_url), callback=self.parse_content ,meta={'item': item})

    def getData(self,item):
        data = pd.read_html(item['product_url'],encoding='utf8')
        for item in data:
            if item.shape[0] > 15:
                data = item
                break
        data.drop(index=data[data[0] == data[1]].index,inplace=True)

        dict_loader = {}
        iter = 0
        for id, item in data.iterrows():
            if item[0] in dict_loader.keys():
                iter  += 1
                dict_loader[f'{item[0]}_{iter}'] = item[1]
            else:
                dict_loader[item[0]] = item[1]

        return dict_loader

    def parse_content(self, response):
        try:
            item = response.meta['item']
            item['image_url'] = response.xpath('//div[@class="img-item"]//img/@src').get()
            item['product_name'] = response.xpath(' //div[@class="product_detail-title"]/h1/text()').get()
            price = response.xpath('//span[@class="gia-km-cu"]/text()').get()
            if type(price) == str:
                price = price.replace('₫','').replace('.','')
            item['price'] = price
            item.update(self.getData(item))

            hnncmp_collections.insert_one(item)
        except Exception as e:
            print(e)
        # return item