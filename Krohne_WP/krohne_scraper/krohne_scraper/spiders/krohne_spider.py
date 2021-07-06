import scrapy
import os
import json

class KrohneSpiders(scrapy.Spider):
    name = "krohne"
    if not os.path.exists('../files'):
        os.makedirs('../files')
    urls = []
    if os.path.isfile('../files/product_urls.json'):
        f_in = open('../files/product_urls.json', 'r')
        products = json.load(f_in)
        for product in products:
            urls.append(products[product])

    else:
        urls = ['https://de.krohne.com/de/produkte/']


    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        if response.url == 'https://de.krohne.com/de/produkte/':
            with open('../files/krohne-produkte.html', 'wb') as f:
                f.write(response.body)
        else:
            if not os.path.exists('../files/urls'):
                os.makedirs('../files/urls')
            splitted_url = response.url.split("/")
            prod = splitted_url[-2]
            prod_type = splitted_url[-5]
            filename = f'{prod_type}_{prod}.html'
            with open('../files/urls/'+filename, 'wb') as f:
                f.write(response.body)
