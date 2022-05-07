# get url file from web
python3 src/utils/make_url_cellphones.py
python3 src/utls/make_url_tgdd.py
cd Crawl

# crawl cellphones
scrapy crawl cellphones
#crawl the gioi di dong
scrapy crawl tgdd