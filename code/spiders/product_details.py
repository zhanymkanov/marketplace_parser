import copy
from datetime import date

import scrapy
from decouple import config

from .constants import HEADER_PRODUCTS


class DetailsSpider(scrapy.Spider):
    page = 1
    allowed_domains = ['kaspi.kz']
    start_urls = [
        'https://kaspi.kz/shop/p/samsung-galaxy-a50-4-64gb-black-1004767/?c=750000000v=specifications'
    ]
    url = config('API_LIST_URL')
    referer_link = config('referer_link')

    def __init__(self, file_name, stop_if_no_reviews=True):
        super().__init__()
        self.file_name = file_name
        self.headers = copy.deepcopy(HEADER_PRODUCTS)
        self.stop_if_no_reviews = stop_if_no_reviews

    def parse(self, response):
        result = {}
        elms3 = response.xpath('.//dl[contains(@class,"specifications-list__spec")]')
        for elm in elms3:
            label = elm.xpath(
                './/span[contains(@class,"specifications-list__'
                'spec-term-text")]/text()').extract_first()
            value = elm.xpath(
                './/dd[contains(@class,"specifications-list__spec-definition")]/text()').get()
            result[label] = value

        yield scrapy.Request(
            url=response.url,
            callback=self.parse_individual_tabs,
            meta={'data': result}
        )

    def parse_individual_tabs(self, response):
        data = response.meta['data']
        yield data


class SmartphoneDetailsSpider(DetailsSpider):
    name = 'smartphones-list-charact'
    file_name = 'smartphones-list.json'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': f'../data/products/{date.today()}/{name}.json',
        'FEED_EXPORT_ENCODING': "utf-8"

    }

    def __init__(self):
        super().__init__(self.file_name)
