from scrapy import Spider, Request
import json
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

nc_collections = database['nguyen_cong']


class NguyenCong(Spider):
    name = 'mama'
    base_url = 'https://nguyencongpc.vn/laptop?page={}'

    def start_requests(self):
        yield Request(url=self.base_url.format(1), callback=self.parse_items)

    def parse_items(self, response):
        print(response.url)
        current_page = response.xpath('//*[@class="paging"]/a[@class="current"]/text()').get().strip()
        all_pages = response.xpath('//*[@class="paging"]/a/text()').getall()
        all_pages = [example.strip() for example in all_pages]

        list_urls = response.xpath('//*[@class="p-container"]/a/@href').getall()
        print(list_urls)
        for url in list_urls:
            yield Request(url=url, callback=self.parse_content)

        print('\n\n\n')
        print(all_pages)
        print(current_page)
        print('\n\n\n\n')
        if all_pages[-1] != current_page:
            yield Request(url=self.base_url.format(int(current_page) + 1), callback=self.parse_items)

    def parse_content(self, response):
        data = {
            'device': 'laptop',
            'url': response.url,
            'item_name': response.xpath('//*[@class="header-product-detail"]/h1/text()').get(),
            'price': response.xpath('//*[@class="detail-price"]/span/text()').getall(),
            'more_offer': response.xpath('//*[@style="white-space: pre-line"]/p/text()').getall(),
            'device_detail_infor': response.xpath('//*[@class="spec-ct"]/table/tbody/tr/td/text()').getall()[4:],
            'salient characteristic': response.xpath('//*[@class="ct-des nd"]/p/text()').getall()
        }
        nc_collections.insert_one(data)


