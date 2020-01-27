import copy
import json
from datetime import date

import scrapy
from decouple import config
from .constants import HEADER_PRODUCTS
from scrapy.loader import ItemLoader
from items.smartphone_charact import Smartphone_charact

class CharactSpider(scrapy.Spider):
    page = 1
    allowed_domains =['kaspi.kz']
    start_urls = [
        'https://kaspi.kz/shop/p/samsung-galaxy-a50-4-64gb-black-1004767/?c=750000000v=specifications'
    ]
    url = config('API_LIST_URL')
    referer_link = config('referer_link')

    def __init__(self, file_name, stop_if_no_reviews=True):
        super().__init__()
        self.file_name = file_name
        # self.url = self.url.format(category=category, page='{}')
        self.headers = copy.deepcopy(HEADER_PRODUCTS)
        # self.headers['Referer'] = self.referer_link.format(category)
        # self.category = category
        self.stop_if_no_reviews = stop_if_no_reviews

    def parse(self, response):
        print("--------THERE_----------")
        # with open(self.file_name) as json_file:
        #     data = json.load(json_file)
        #     print(data)
        items = Smartphone_charact()
        result = {}
        elms3 = response.xpath('.//dl[contains(@class,"specifications-list__spec")]')
        for elm in elms3:
            result[elm.xpath('.//span[contains(@class,"specifications-list__spec-term-text")]/text()').extract_first()] = elm.xpath('.//dd[contains(@class,"specifications-list__spec-definition")]/text()').get()[1:]

        #  Код снизу для использорвания Item

        #//*[@id="specifications"]/div/dl[1]/dd/dl[1]/dd
        # print(response.text)
        # # print(response.xpath('//dd[@class="specifications-list__spec-definition"]/text()').get())
        # # items['type'] = response.xpath('//div[@id="specifications"]/div/dl[1]/dd/dl[1]/dd/text()').get()
        # items['type'] = response.xpath('//li[@class="short-specifications__list-el"]/text()').get()
        #
        # items['standard'] = result[2]
        # yield items
        yield scrapy.Request(
            url=response.url,
            callback=self.parse_individual_tabs,
            meta={'data': result}
        )


        # elms = response.xpath('.//li[contains(@class, "short-specifications__list-el")]/text()').getall()
        # for elm in elms:
        #     print(elm)
        # yield result


    def parse_individual_tabs(self, response):
        data = response.meta['data']
        yield data

class SmartphoneCharactSpider(CharactSpider):
    name = 'smartphones-list-charact'
    file_name = 'smartphones-list.json'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': f'../data/products/{date.today()}/{name}.json'
    }
    def __init__(self):
        super().__init__(self.file_name)



