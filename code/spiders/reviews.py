import scrapy
import json
import os
import datetime as dt
from decouple import config
import logging


class ReviewsSpider(scrapy.Spider):
    url = config('API_REVIEWS_URL')
    headers = {
        "Accept": "application/json, text/*", "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru,en;q=0.9,kk;q=0.8,es;q=0.7,ba;q=0.6", "Connection": "keep-alive",
        "Host": "kaspi.kz", "Cache-Control": "no-cache, no-store, max-age=0"
    }

    def __init__(self, category):
        super().__init__()
        self.category = category

        today = str(dt.date.today())
        self.OUTPUT_DATE = today

        if os.path.exists(f'../data/products/{today}'):
            self.PARSE_DATE = today
        else:
            self.PARSE_DATE = '2019-12-13'
            self.logger.warning(f'Path ../data/products/{today} does not exist, 2019-12-13 is used')

        self.PARSE_FILE = f'../data/products/{self.PARSE_DATE}/{category}-list.json'
        self.OUTPUT_DATE = f'../data/reviews/{self.OUTPUT_DATE}/{category}'
        os.makedirs(self.OUTPUT_DATE, exist_ok=True)

        self.log(f"Parser for {self.category} has been started.")

    def start_requests(self):
        with open(self.PARSE_FILE) as products_json:
            products = json.load(products_json)
            for product in products:
                id, reviews_quantity = product['id'], 4000
                if product['reviewsQuantity']:
                    yield scrapy.Request(
                        url=self.url.format(id, reviews_quantity),
                        headers=self.headers,
                        callback=self.parse_reviews,
                        cb_kwargs={'id': id, 'reviews_quantity': product['reviewsQuantity']}
                    )

    def parse_reviews(self, response, id, reviews_quantity):
        data = response.body_as_unicode()
        with open(f'{self.OUTPUT_DATE}/{id}.json', 'w') as f:
            f.write(data)

        data = json.loads(data)
        if reviews_quantity != len(data['data']):
            self.logger.warning(f'Product with id={id} received {len(data["data"])} reviews, but has {reviews_quantity}')


class BeautySpider(ReviewsSpider):
    name = "beauty-reviews"
    category = "beauty"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class BigHomeAppSpider(ReviewsSpider):
    name = "bha-reviews"
    category = "big-home-appl"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class SmallHomeAppSpider(ReviewsSpider):
    name = "sha-reviews"
    category = "small-home-appl"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class KitchenHomeAppSpider(ReviewsSpider):
    name = "kha-reviews"
    category = "kitchen-home-appl"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class ClimateEquipmentSpider(ReviewsSpider):
    name = "climate-reviews"
    category = "climate-equipment"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class BooksSpider(ReviewsSpider):
    name = "books-reviews"
    category = "books"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class HeadphonesSpider(ReviewsSpider):
    name = "headphones-reviews"
    category = "headphones"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class PerfumesSpider(ReviewsSpider):
    name = "perfumes-reviews"
    category = "perfumes"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class CarAudioSpider(ReviewsSpider):
    name = "car-audio-reviews"
    category = "car-audio"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class CarElectronicsSpider(ReviewsSpider):
    name = "car-electronics-reviews"
    category = "car-electronics"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class MemoryCardsSpider(ReviewsSpider):
    name = "memory-cards-reviews"
    category = "memory-cards"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class PowerBanksSpider(ReviewsSpider):
    name = "power-banks-reviews"
    category = "power-banks"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class TiresSpider(ReviewsSpider):
    name = "tires-reviews"
    category = "tires"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class WatchesSpider(ReviewsSpider):
    name = "watches-reviews"
    category = "watches"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class WearablesSpider(ReviewsSpider):
    name = "wearables-reviews"
    category = 'wearables'
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class SmartphonesSpider(ReviewsSpider):
    name = "smartphones-reviews"
    category = "smartphones"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)


class PortableSpeakersSpider(ReviewsSpider):
    name = "portable-speakers-reviews"
    category = "portable-speakers"
    custom_settings = {
        'LOG_FILE': f'{name}.log'
    }
    logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        super().__init__(self.category)
