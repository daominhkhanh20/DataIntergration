from ast import Yield
from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd

client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database =client['ProcessData']
laptopworld_collections = database['laptopworld']


class LaptopWorld1(Spider):
    name = 'laptopworld1'
    base_url = 'https://laptopworld.vn/{}'


    def start_requests(self):
        device = 'laptop'

        urls = 'https://laptopworld.vn/may-tinh-xach-tay.html?page={}'
        for page in range(1,28):
            yield Request(url=urls.format(page), callback=self.parse)
                
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

    def parse(self, response):
        base_url = 'https://laptopworld.vn{}'
        list_url = response.xpath('//div[@class="p-container"]/a[@class="p-img"]/@href').getall()

        if len(list_url):
            for detail_url in list_url:
                detail_url = base_url.format(detail_url)
                if detail_url is not None:
                    item = {
                        'device': 'laptop',
                        'product_url': detail_url
                    }

                    request = Request(response.urljoin(detail_url), callback=self.parse_content)
                    request.meta['item'] = item
                    yield request
                        
        
    def parse_content(self, response):
        try:
            if ("Phụ kiện" in response.xpath('//section[@class="link-url"]//span/text()').getall()[-1]):
                return

            base_url = 'https://laptopworld.vn'
            item = response.meta['item']
            item['image_url']=  [base_url + x for x in response.xpath('//div[@id="img-large"]//div[@class="item"]/a/@href').getall()[1:]][0]
            item['product_name'] =  response.xpath('//div[@class="content-top-detail-left"]/h1/text()').get()
            price = response.xpath('//div[@id="wrap-product-price"]//span[@class="price-border"]/text()').get()
            if type(price) == str:
                price = price.replace('₫','').replace('.','')
            item['price'] = price
            item.update(self.getData(item))
            laptopworld_collections.insert_one(item)
            print(item)
        except Exception as e:
            print(e)



