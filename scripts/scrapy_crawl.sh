# get url file from web
python3 src/utils/make_url_cellphones.py
python3 src/utls/make_url_tgdd.py
cd Crawl/Scrapy

crawl cellphones
scrapy crawl cellphones
#crawl the gioi di dong
scrapy crawl tgdd

scrapy crawl phongvu -O ../Url/phongvu/phongvu_phone_url.json -a device=phone
scrapy crawl phongvu -O ../Url/phongvu/phongvu_laptop_url.json -a device=laptop
scrapy crawl anphat

cd ../api
python phongvu_extract.py

#crawl phucanh
scrapy crawl phucanh
#crawl laptopworld
scrapy crawl laptopworld