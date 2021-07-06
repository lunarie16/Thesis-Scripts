echo "crawling main page for product urls"
cd krohne_scraper
scrapy crawl krohne
cd ..
python extract_urls.py
echo "crawling all product pages"
cd krohne_scraper
scrapy crawl krohne
cd ..
python crawl_descriptions.py
