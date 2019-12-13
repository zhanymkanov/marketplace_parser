import scrapy
import json
import os
import datetime as dt
from decouple import config


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
        self.PARSE_DATE = today if os.path.exists(f'../data/products/{today}') else '2019-11-19'
        self.OUTPUT_DATE = today
        self.INPUT_FILE = f'../data/products/{self.PARSE_DATE}/{category}-list.json'
        self.OUTPUT_DATE = f'../data/reviews/{self.OUTPUT_DATE}/{category}'

    def start_requests(self):
        os.makedirs(self.OUTPUT_DATE, exist_ok=True)

        with open(self.INPUT_FILE) as products_json:
            products = json.load(products_json)
            for product in products:
                id, reviews_quantity = product['id'], product['reviewsQuantity'] + (product['reviewsQuantity'] >> 1)
                if reviews_quantity:
                    yield scrapy.Request(
                        url=self.url.format(id, reviews_quantity),
                        headers=self.headers,
                        callback=self.parse_reviews,
                        cb_kwargs={'id': id}
                    )

    def parse_reviews(self, response, id):
        data = response.body_as_unicode()
        with open(f'{self.OUTPUT_DATE}/{id}.json', 'w') as f:
            f.write(data)


class BeautyReviewsSpider(ReviewsSpider):
    name = "beauty-reviews"
    category = "beauty"

    def __init__(self):
        super().__init__(self.category)


class BigHomeAppReviewsSpider(ReviewsSpider):
    name = "bha-reviews"
    category = "bha"

    def __init__(self):
        super().__init__(self.category)


class SmallHomeAppReviewsSpider(ReviewsSpider):
    name = "sha-reviews"
    category = "sha"

    def __init__(self):
        super().__init__(self.category)


class KitchenHomeAppReviewsSpider(ReviewsSpider):
    name = "kha-reviews"
    category = "kha"

    def __init__(self):
        super().__init__(self.category)


class ClimateEquipmentReviewsSpider(ReviewsSpider):
    name = "climate-reviews"
    category = "climate"

    def __init__(self):
        super().__init__(self.category)


class BooksReviewsSpider(ReviewsSpider):
    name = "books-reviews"
    category = "books"

    def __init__(self):
        super().__init__(self.category)


class HeadphonesReviewsSpider(ReviewsSpider):
    name = "headphones-reviews"
    category = "headphones"

    def __init__(self):
        super().__init__(self.category)


class PerfumesReviewsSpider(ReviewsSpider):
    name = "perfumes-reviews"
    category = "perfumes"

    def __init__(self):
        super().__init__(self.category)


class CarAudioReviewsSpider(ReviewsSpider):
    name = "car-audio-reviews"
    category = "car-audio"

    def __init__(self):
        super().__init__(self.category)


class CarElectronicsReviewsSpider(ReviewsSpider):
    name = "car-electronics-reviews"
    category = "car-electronics"

    def __init__(self):
        super().__init__(self.category)


class MemoryCardsReviewsSpider(ReviewsSpider):
    name = "memory-cards-reviews"
    category = "memory-cards"

    def __init__(self):
        super().__init__(self.category)


class PowerBanksReviewsSpider(ReviewsSpider):
    name = "power-banks-reviews"
    category = "power-banks"

    def __init__(self):
        super().__init__(self.category)


class TiresReviewsSpider(ReviewsSpider):
    name = "tires-reviews"
    category = "tires"

    def __init__(self):
        super().__init__(self.category)


class WatchesReviewsSpider(ReviewsSpider):
    name = "watches-reviews"
    category = "watches"

    def __init__(self):
        super().__init__(self.category)


class WearablesReviewsSpider(ReviewsSpider):
    name = "wearables-reviews"
    category = 'wearables'

    def __init__(self):
        super().__init__(self.category)


class SmartphonesReviewsSpider(ReviewsSpider):
    name = "smartphones-reviews"
    category = "smartphones"

    def __init__(self):
        super().__init__(self.category)
