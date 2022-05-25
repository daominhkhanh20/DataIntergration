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

        for page in range(1,5):
            yield Request(url=urls.format(page), callback=self.parse)
        # if device == 'laptop':
        #     urls = 'https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html?page={}'

        #     for page in range(1,19):
        #         yield Request(url=urls.format(page), callback=self.parse)
        # elif device == 'phone':
        #     urls = 'https://phongvu.vn/dien-thoai-cat.2389'

        #     yield Request(url=urls, callback=self.parse)
        
    def parse(self, response):
        base_url = 'https://www.anphatpc.com.vn{}'
        list_url =  response.xpath('//div[@class="p-item "]/a/@href').getall()
        if len(list_url):
            for detail_url in list_url:
                detail_url = base_url.format(detail_url)
                if detail_url is not None:
                    item = {
                        # 'device':'laptop',
                        'url': detail_url,
                    }
                    yield item
                    # request = Request(response.urljoin(detail_url), callback=self.parse_content)
                    # request.meta['item'] = item
                    # yield request

    def parse_content(self, response):
        item = response.meta['item']
        item['image_url'] = response.xpath('//img[@class="lazyload css-jdz5ak"]/@src').get()
        item['item_name'] = response.xpath('//h1[@class="css-4kh4rf"]/text()').get()
        item['price'] = response.xpath('//div[@class="css-12htb1n"]/div[@class="css-152xv71"]/text()').get()
        item['device_detail_infor'] = response.xpath('//div[@class="css-1i3ajxp"]/div[@class="css-bz0ypq"]/text()').getall()
        # item['content'] = response.xpath('//article[@class="fck_detail "]/p[@class="Normal"]//text()').extract()
        # item['url_image'] = response.xpath('//img[@itemprop="contentUrl"]/@data-src').extract()
        # item['description'] = response.xpath('//p[@class="description"]/text()').get()
        # item['author'] = response.xpath('//h3[@class="title-news"]/a/text()').get()
        # item['author_role'] = response.xpath('//div[@class="sum-info"]/p[@class="description"]/text()').get()
        # item['author_image'] = response.xpath('//a[@class="thumb thumb-1x1 thumb-circle"]/img/@src').get()
        # item['relation_link'] = response.xpath('//div[@class="width_common list-news-subfolder"]/article/h4/a/@href').extract()
        # pv_collections.insert_one(item)
        return item