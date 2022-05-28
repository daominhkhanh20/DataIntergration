from ast import Yield
from scrapy import Spider, Request
from pymongo import MongoClient

client = MongoClient("mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database =client['DataIntegration']
pa_collections = database['nguyenkim']


class Nguyenkim(Spider):
        name = 'nguyenkim'
        base_url = 'https://www.nguyenkim.com/{}'


        def start_requests(self):
            device = 'phone'

            urls = 'https://www.nguyenkim.com/dien-thoai-di-dong/page-{}/'
            for page in range(1,8):
                yield Request(url=urls.format(page), callback=self.parse)
                
        

        def parse(self, response):
            base_url = 'https://www.phucanh.vn/{}'
            list_url = response.xpath('//div[@class="item-list product"]/div[@class="product-body"]/div[@class="product-title"]/a/@href').getall()

            if len(list_url):
                for url in list_url:
                    #detail_url = base_url.format(detail_url)
                    if url is not None:
                        item = {
                            'device': 'phone',
                            'url': url
                        }

                        #yield item

                        request = Request(response.urljoin(url), callback=self.parse_content)
                        request.meta['item'] = item
                        yield request
                        
        
        def parse_content(self, response):
            item = response.meta['item']
            item['image_url']=  response.xpath('//div[@class="wrap-img-tag-pdp"]/img/@src').getall()
            item ['item-name'] =  response.xpath('//div[@class="wrap_name_vote"]/h1/text()').get()
            item['price'] = response.xpath('//div[@class="product_info_price_value-final"]/span/text()').get()
            item['device_detail_info'] =   response.xpath('//table[@class="productSpecification_table"]/tbody/tr/td/text()').getall()
            

            
            pa_collections.insert_one(item)
            # yield item

            



