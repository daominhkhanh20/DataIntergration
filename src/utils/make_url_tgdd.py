import json
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

url_laptop = "https://www.thegioididong.com/Category/FilterProductBox?c=44&o=9&pi={}"
url_phone = "https://www.thegioididong.com/Category/FilterProductBox?c=42&o=9&pi={}"

def save_file(data, file_name):
    with open(file_name, 'w+') as file:
        json.dump(data, file, indent=4)


def get_laptop_url_item(url: str, max_page: int, file_name: str):
    final_data = []
    for i in tqdm(range(0, max_page)):
        url_temp = url.format(i)
        response = requests.get(url_temp, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            })
        data = json.loads(response.text)
        soup = BeautifulSoup(data["listproducts"])
        for link in soup.find_all('a'):
            if ("/laptop" in link.get('href')):
                url_item = "https://www.thegioididong.com"+ link.get('href')
                final_data.append(url_item)
    save_file(final_data, file_name)

def get_phone_url_item(url: str, max_page: int, file_name: str):
    final_data = []
    for i in tqdm(range(0, max_page)):
        url_temp = url.format(i)
        response = requests.get(url_temp, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            })
        data = json.loads(response.text)
        soup = BeautifulSoup(data["listproducts"])
        for link in soup.find_all('a'):
            has_one_variant = True
            for sub_link in link.find_all('li'):
                if (sub_link.get('data-url') is None):
                    continue
                if ("/dtdd" in sub_link.get('data-url')):
                    url_item = "https://www.thegioididong.com"+ sub_link.get('data-url')
                    final_data.append(url_item)
                    has_one_variant = False
            if (has_one_variant == True):
                if ("/dtdd" in link.get('href')):
                    url_item = "https://www.thegioididong.com"+ link.get('href')
                    final_data.append(url_item)
    save_file(final_data, file_name)

get_phone_url_item(url_phone, max_page=5, file_name="Crawl/Url/tgdd/phone.json")
get_laptop_url_item(url_laptop, max_page=14, file_name='Crawl/Url/tgdd/laptop.json')
