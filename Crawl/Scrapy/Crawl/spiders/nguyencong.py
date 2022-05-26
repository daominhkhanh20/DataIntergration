from scrapy import Spider, Request
import json
from pymongo import MongoClient
import re

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

nc_collections = database['nguyen_cong']


def parse(sent):
    results = re.findall('>.*?<', sent)
    final = []
    for example in results:
        example = example.replace('\n', "").strip()
        example = example.replace('\r', "").strip()
        example = example.replace('>', "").strip()
        example = example.replace('<', "").strip()
        if example != "":
            final.append(example)
    return final


class NguyenCong(Spider):
    name = 'nguyencong'
    base_url = 'https://nguyencongpc.vn/laptop?page='

    def start_requests(self):
        yield Request(url=self.base_url + str(1), callback=self.parse_items)

    def parse_items(self, response):
        print(response.url)
        current_page = response.xpath('//*[@class="paging"]/a[@class="current"]/text()').get().strip()
        all_pages = response.xpath('//*[@class="paging"]/a/text()').getall()
        all_pages = [example.strip() for example in all_pages]

        list_urls = response.xpath('//*[@class="p-container"]/a/@href').getall()
        for url in list_urls:
            yield response.follow(url=url, callback=self.parse_content)

        if all_pages[-1] != current_page:
            yield Request(url=self.base_url + str(int(current_page) + 1), callback=self.parse_items)

    def parse_content(self, response):
        data = {
            'device': 'laptop',
            'url': response.url,
            'item_name': response.xpath('//*[@class="header-product-detail"]/h1/text()').get(),
            'price': response.xpath('//*[@class="detail-price"]/span/text()').getall(),
            'more_offer': response.xpath('//*[@style="white-space: pre-line"]/p/text()').getall(),
            'salient characteristic': response.xpath('//*[@class="ct-des nd"]/p/text()').getall()
        }
        device_info_elements = response.xpath('//*[@class="spec-ct"]/table/tbody/tr/td').getall()
        information = []
        for element in device_info_elements:
            result_parse = parse(element)
            if len(result_parse) != 0:
                information.append(result_parse)

        data['device_detail_infor'] = information
        nc_collections.insert_one(data)
