import json
from datetime import date

import scrapy
from decouple import config

from .constants import PRODUCTS_DIR
from .utils import get_parse_date


class DetailsSpider(scrapy.Spider):
    referer_link = config('referer_link')

    def __init__(self, category):
        super().__init__()
        parse_date = get_parse_date(PRODUCTS_DIR)
        self.products_json = f'{PRODUCTS_DIR}/{parse_date}/{category}-list.json'

    def start_requests(self):
        with open(self.products_json) as products_json:
            products = json.load(products_json)
            for product in products:
                url = product['shopLink']
                yield scrapy.Request(
                    url=url,
                    cb_kwargs={'product': product},
                    callback=self.parse_product
                )

    def parse_product(self, response, product):
        """
        dl - is the block
        dt - is the header
        dd - is the body

        dd may be the root of other dls
        """
        details = {}
        blocks = response.xpath('//dl[contains(@class,"specifications-list__spec")]')
        for block in blocks:
            characteristic = block.xpath('dt/span/text()').get()
            value = block.xpath('dd/text()').get()

            details[characteristic] = value

        yield {
            'id': product['id'],
            'title': product['title'],
            'url': product['shopLink'],
            'brand': product['brand'],
            'rating': product['adjustedRating'],
            'reviews_quantity': product['reviewsQuantity'],
            'price': product['unitSalePrice'],
            'category_id': product['categoryId'],
            'category_name': product['categoryName'],
            'parsed_details': details
        }


class SmartphoneDetailsSpider(DetailsSpider):
    name = 'smartphones-details'
    category = 'smartphones'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': "utf-8",
        'FEED_URI': f'../data/products/{date.today()}/{name}.json',
    }

    def __init__(self):
        super().__init__(self.category)


class ComputerDetailsSpider(DetailsSpider):
    name = 'computers-details'
    category = 'computers'
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': "utf-8",
        'FEED_URI': f'../data/products/{date.today()}/{name}.json',
    }

    def __init__(self):
        super().__init__(self.category)
