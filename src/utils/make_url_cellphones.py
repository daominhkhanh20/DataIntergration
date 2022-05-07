import json
from tqdm import tqdm
import requests

url_phone = "https://cellphones.com.vn/lapi/LoadMoreProductCate/index/?page={" \
            "}&id=3&order=view_count2&dir=desc&fearture=flashsale_samsung "
url_laptop = "https://cellphones.com.vn/lapi/LoadMoreProductCate/index/?page={" \
             "}&id=380&order=view_count2&dir=desc&fearture=flashsale_laptop "


def save_file(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)


def get_url_item(url: str, max_page: int, file_name: str):
    final_data = []
    for i in tqdm(range(1, max_page)):
        try:
            url_temp = url.format(i)
            response = requests.get(url_temp)
            data = json.loads(response.text)
            final_data.append(data)
        except:
            print('error')

    list_url_item = []
    for example in final_data:
        for item in example:
            list_url_item.append(item['url'])

    print(len(list_url_item))
    save_file(list_url_item, file_name)


get_url_item(url_phone, max_page=200, file_name='Crawl/Url/cellphones/phone.json')
get_url_item(url_laptop, max_page=200, file_name='Crawl/Url/cellphones/laptop.json')
