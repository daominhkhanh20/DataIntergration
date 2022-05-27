from ast import Yield
from scrapy import Spider, Request
from pymongo import MongoClient

client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database =client['DataIntegration']
laptopworld_collections = database['laptopworld']


class LaptopWorld(Spider):
    name = 'laptopworld'
    base_url = 'https://laptopworld.vn/{}'


    def start_requests(self):
        device = 'laptop'

        urls = 'https://laptopworld.vn/may-tinh-xach-tay.html?page={}'
        for page in range(1,28):
            yield Request(url=urls.format(page), callback=self.parse)
                
        

    def parse(self, response):
        base_url = 'https://laptopworld.vn{}'
        list_url = response.xpath('//div[@class="p-container"]/a[@class="p-img"]/@href').getall()

        if len(list_url):
            for detail_url in list_url:
                detail_url = base_url.format(detail_url)
                if detail_url is not None:
                    item = {
                        'device': 'laptop',
                        'url': detail_url
                    }

                    request = Request(response.urljoin(detail_url), callback=self.parse_content)
                    request.meta['item'] = item
                    yield request
                        
        
    def parse_content(self, response):
        if ("Phụ kiện" in response.xpath('//section[@class="link-url"]//span/text()').getall()[-1]):
            return
        base_url = 'https://laptopworld.vn'
        item = response.meta['item']
        item['image_url']=  [base_url + x for x in response.xpath('//div[@id="img-large"]//div[@class="item"]/a/@href').getall()[1:]]
        item['item-name'] =  response.xpath('//div[@class="content-top-detail-left"]/h1/text()').get()
        item['price'] = response.xpath('//div[@id="wrap-product-price"]//span[@class="price-border"]/text()').get()
        item['device_detail_info'] = response.xpath('//div[@id="tab1"]/div[@class="content-text nd"]//tr/td//span//text()').getall()
        item['more_offer'] = [text.strip() for text in response.xpath('//div[@class="product-offer"]/div[@class="content"]//text()').getall() if text.strip()]
        item['salient characteristic'] = [text.strip() for text in response.xpath('//div[@id="tab2"]/div[@class="content-text nd"]//text()').getall() if text.strip()]

        laptopworld_collections.insert_one(item)



