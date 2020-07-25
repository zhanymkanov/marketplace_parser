import json
import os
from datetime import date

import scrapy
from decouple import config

from app.constants import HEADER_REVIEWS, PRODUCTS_DIR, REVIEWS_DIR
from app.utils import parse_latest_date

REVIEWS_PER_REQUEST = 5000


class ReviewsSpider(scrapy.Spider):
    url = config("API_REVIEWS_URL")

    def __init__(self, category):
        super().__init__()
        self.category_reviews_dir = self._get_category_reviews_dir(category)
        self.category_products = self._get_products_list(category)
        self.log(f"Parser for {category} reviews has been started.")

    def start_requests(self):
        for product in self.category_products:
            yield scrapy.Request(
                url=self.url.format(product["source_id"], REVIEWS_PER_REQUEST),
                headers=HEADER_REVIEWS,
                callback=self.write_product_reviews,
                cb_kwargs={
                    "product_id": product["source_id"],
                },
            )

    def write_product_reviews(self, response, product_id):
        reviews_json = response.body_as_unicode()
        with open(f"{self.category_reviews_dir}/{product_id}.json", "w") as f:
            f.write(reviews_json)

    @staticmethod
    def _get_category_reviews_dir(category):
        category_dir = f"{REVIEWS_DIR}/{date.today()}/{category}"
        os.makedirs(category_dir, exist_ok=True)

        return category_dir

    @staticmethod
    def _get_products_list(category):
        parse_date = parse_latest_date(PRODUCTS_DIR)
        category_products = f"{PRODUCTS_DIR}/{parse_date}/{category}-list.json"

        with open(category_products) as category_products:
            products = json.load(category_products)

        return products


class ComputersSpider(ReviewsSpider):
    name = "computers-reviews"
    category = "computers"

    def __init__(self):
        super().__init__(self.category)


class BeautySpider(ReviewsSpider):
    name = "beauty-reviews"
    category = "beauty"

    def __init__(self):
        super().__init__(self.category)


class BigHomeAppSpider(ReviewsSpider):
    name = "bha-reviews"
    category = "big-home-appl"

    def __init__(self):
        super().__init__(self.category)


class SmallHomeAppSpider(ReviewsSpider):
    name = "sha-reviews"
    category = "small-home-appl"

    def __init__(self):
        super().__init__(self.category)


class KitchenHomeAppSpider(ReviewsSpider):
    name = "kha-reviews"
    category = "kitchen-home-appl"

    def __init__(self):
        super().__init__(self.category)


class ClimateEquipmentSpider(ReviewsSpider):
    name = "climate-reviews"
    category = "climate-equipment"

    def __init__(self):
        super().__init__(self.category)


class BooksSpider(ReviewsSpider):
    name = "books-reviews"
    category = "books"

    def __init__(self):
        super().__init__(self.category)


class HeadphonesSpider(ReviewsSpider):
    name = "headphones-reviews"
    category = "headphones"

    def __init__(self):
        super().__init__(self.category)


class PerfumesSpider(ReviewsSpider):
    name = "perfumes-reviews"
    category = "perfumes"

    def __init__(self):
        super().__init__(self.category)


class CarAudioSpider(ReviewsSpider):
    name = "car-audio-reviews"
    category = "car-audio"

    def __init__(self):
        super().__init__(self.category)


class CarElectronicsSpider(ReviewsSpider):
    name = "car-electronics-reviews"
    category = "car-electronics"

    def __init__(self):
        super().__init__(self.category)


class MemoryCardsSpider(ReviewsSpider):
    name = "memory-cards-reviews"
    category = "memory-cards"

    def __init__(self):
        super().__init__(self.category)


class PowerBanksSpider(ReviewsSpider):
    name = "power-banks-reviews"
    category = "power-banks"

    def __init__(self):
        super().__init__(self.category)


class TiresSpider(ReviewsSpider):
    name = "tires-reviews"
    category = "tires"

    def __init__(self):
        super().__init__(self.category)


class WatchesSpider(ReviewsSpider):
    name = "watches-reviews"
    category = "watches"

    def __init__(self):
        super().__init__(self.category)


class WearablesSpider(ReviewsSpider):
    name = "wearables-reviews"
    category = "wearables"

    def __init__(self):
        super().__init__(self.category)


class SmartphonesSpider(ReviewsSpider):
    name = "smartphones-reviews"
    category = "smartphones"

    def __init__(self):
        super().__init__(self.category)


class PortableSpeakersSpider(ReviewsSpider):
    name = "portable-speakers-reviews"
    category = "portable-speakers"

    def __init__(self):
        super().__init__(self.category)
