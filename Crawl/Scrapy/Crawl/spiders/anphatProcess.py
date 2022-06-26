from scrapy import Spider, Request
from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    "mongodb+srv://dataintergration:nhom10@cluster0.hqw7c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['ProcessData']

ap_collections = database['anphat']

class AnPhat(Spider):
    name = 'anphatPd'

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

    # def getData(self,item):
    #     data = pd.read_html(item['product_url'],encoding='utf8')
    #     data = data[1]
    #     data.drop(index=data[data[0] == data[1]].index,inplace=True)
    #     list_type = ['Tên sản phẩm','Hệ điều hành\xa0(bản quyền) đi kèm','Dung lượng','Bộ vi xử lý','Card màn hình','Dung lượng','Trọng Lượng','Xuất xứ','Hãng sản xuất','Màu sắc','Kiểu Pin']
    #     dict_tmp = {'Tên sản phẩm':'product_name','Hệ điều hành\xa0(bản quyền) đi kèm':'os','Bộ vi xử lý':'cpu','Card màn hình':'gpu','Trọng Lượng':'weight','Xuất xứ':'origin','Hãng sản xuất':'brand','Màu sắc':'color','Kiểu Pin':'pin'}
        
    #     dict_loader = {}
    #     list_need = ['product_name', 'os','ram', 'cpu','cpu speed' ,'gpu', 'screen','screen resolution','storage','weight', 'origin', 'brand', 'color', 'pin']
    #     for x in list_need:
    #         dict_loader[x] = ''

    #     for id, item in data.iterrows():
    #         if (item[0] == 'Dung lượng' and item[1][2:4] == 'GB') or item[0] == 'RAM':
    #             dict_loader['ram'] = item[1]
    #         elif item[0] == 'Dung lượng' and item[1][2:4] != 'GB':
    #             dict_loader['storage'] = item[1]
    #         elif item[0] == 'Công nghệ CPU':
    #             dict_loader['cpu'] = item[1]
    #         elif item[0] == 'Xuất Xứ':
    #             dict_loader['origin'] = item[1]
    #         elif  item[0] in ['Tốc độ','Tốc độ CPU']:
    #             dict_loader['cpu speed'] = item[1]
    #         elif item[0] in ['Công nghệ màn hình','Màn hình']:
    #             dict_loader['screen'] = item[1]
    #         elif item[0] in ['Độ phân giải']:
    #             dict_loader['screen resolution'] = item[1]
            
    #         elif item[0] in list_type:
    #             dict_loader[dict_tmp[item[0]]] = item[1]
    #     return dict_loader
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
            item['product_name'] = response.xpath('//h1[@class="pro-name js-product-name"]/text()').get()
            item['image_url'] = response.xpath('//span[@class="img"]/img[@class="fit-img"]/@src').get()
            item['price'] = response.xpath('//b[@class="text-18 js-pro-total-price"]/@data-price').get()
            item.update(self.getData(item))

            ap_collections.insert_one(item)
        except Exception as e:
            print(e)
            # return item