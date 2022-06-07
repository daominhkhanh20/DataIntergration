from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['DataIntegration']

ap_collections = database['ProcessData']

class AnPhat(Spider):
    name = 'anphat2'

    def start_requests(self):
        # device = getattr(self, 'device', None)
        urls = 'https://www.anphatpc.com.vn/may-tinh-xach-tay-laptop.html?page={}'

        for page in range(1,19):
            yield Request(url=urls.format(page), callback=self.parse)
   
        
    def parse(self, response):
        base_url = 'https://www.anphatpc.com.vn{}'
        list_url =  response.xpath('//div[@class="p-item "]/a/@href').getall()
        if len(list_url):
            for detail_url in list_url:
                detail_url = base_url.format(detail_url)
                if detail_url is not None:
                    item = {
                        'device':'laptop',
                        'product_url': detail_url,
                    }

                    yield Request(response.urljoin(detail_url), callback=self.parse_content ,meta={'item': item})

    def getData(self,item):
        data = pd.read_html(item['product_url'],encoding='utf8')
        data = data[1]
        data.drop(index=data[data[0] == data[1]].index,inplace=True)
        list_type = ['Tên sản phẩm','Hệ điều hành\xa0(bản quyền) đi kèm','Dung lượng','Bộ vi xử lý','Card màn hình','Dung lượng','Trọng Lượng','Xuất xứ','Hãng sản xuất','Màu sắc','Kiểu Pin']
        dict_tmp = {'Tên sản phẩm':'product_name','Hệ điều hành\xa0(bản quyền) đi kèm':'os','Bộ vi xử lý':'cpu','Card màn hình':'gpu','Trọng Lượng':'weight','Xuất xứ':'origin','Hãng sản xuất':'brand','Màu sắc':'color','Kiểu Pin':'pin'}
        dict_loader = {}
        for x in dict_tmp.values():
            dict_loader[x] = ''

        for id, item in data.iterrows():
            if (item[0] == 'Dung lượng' and item[1][2:4] == 'GB') or item[0] == 'RAM':
                dict_loader['ram'] = item[1]
            elif item[0] == 'Dung lượng' and item[1][2:4] != 'GB':
                dict_loader['storage'] = item[1]
            elif item[0] == 'Công nghệ CPU':
                dict_loader['cpu'] = item[1]
            elif item[0] == 'Xuất Xứ':
                dict_loader['origin'] = item[1]
            elif item[0] in list_type:
                dict_loader[dict_tmp[item[0]]] = item[1]
        return dict_loader
    def parse_content(self, response):
        item = response.meta['item']
        item['image_url'] = response.xpath('//span[@class="img"]/img[@class="fit-img"]/@src').get()
        item['price'] = response.xpath('//b[@class="text-18 js-pro-total-price"]/@data-price').get()
        item['web'] = 'anphat'
        item.update(self.getData(item))

        ap_collections.insert_one(item)
        # return item