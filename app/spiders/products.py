import copy
import json
from datetime import date

import scrapy
from decouple import config

from app.constants import HEADER_DEFAULT, PRODUCTS_DIR, SPECS_DIR

API_URL = config("PRODUCTS_API")


class ProductsSpider(scrapy.Spider):
    page = 1

    def __init__(self, category):
        super().__init__()
        self.category = category
        self.url = self._get_category_url(category)
        self.headers = self._get_category_headers(category)

    def start_requests(self):
        page_url = self.url.format(self.page)
        yield scrapy.Request(
            page_url,
            callback=self.parse_page_products,
            headers=self.headers,
            dont_filter=True,
        )

    def parse_page_products(self, response):
        page_products = json.loads(response.text)
        page_products = page_products["data"]

        if not page_products:
            return

        for product in page_products:
            yield {
                "source_id": product["id"],
                "title": product["title"],
                "url": product["shopLink"],
                "brand": product["brand"],
                "rating": product["adjustedRating"],
                "reviews_quantity": product["reviewsQuantity"],
                "price_unit": product["unitPrice"],
                "price_sale": product["unitSalePrice"],
                "category_id": product["categoryId"],
                "category_name": self.category,
            }

        yield from self.parse_next_page()

    def parse_next_page(self):
        if self.page > 100:
            return

        self.page += 1
        url = self.url.format(self.page)

        yield scrapy.Request(
            url=url,
            headers=self.headers,
            callback=self.parse_page_products,
            dont_filter=True,
        )

    @staticmethod
    def _get_category_url(category):
        return API_URL.format(category=category, page="{}")

    @staticmethod
    def _get_category_headers(category):
        headers = copy.deepcopy(HEADER_DEFAULT)
        headers["Referer"] = headers["Referer"].format(category)
        return headers


class SmartphonesSpider(ProductsSpider):
    name = "smartphones-list"
    category_link = "smartphones"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class NotebooksSpider(ProductsSpider):
    name = "notebooks-list"
    category_link = "notebooks"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{SPECS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class DesktopsSpider(ProductsSpider):
    name = "desktops-list"
    category_link = "desktops"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{SPECS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class ComputersSpider(ProductsSpider):
    name = "computers-list"
    category_link = "computers"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class BeautySpider(ProductsSpider):
    name = "beauty-list"
    category_link = "beauty%20care%20equipment"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class PerfumeSpider(ProductsSpider):
    name = "perfumes-list"
    category_link = "perfumes"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class BooksSpider(ProductsSpider):
    name = "books-list"
    category_link = "books"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class CarAudioSpider(ProductsSpider):
    name = "car-audio-list"
    category_link = "car%20audio"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class CarElectronicsSpider(ProductsSpider):
    name = "car-electronics-list"
    category_link = "car%20electronics"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class HeadphonesSpider(ProductsSpider):
    name = "headphones-list"
    category_link = "headphones"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class BigHomeAppliancesSpider(ProductsSpider):
    name = "big-home-appl-list"
    category_link = "big%20home%20appliances"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class SmallHomeAppliancesSpider(ProductsSpider):
    name = "small-home-appl-list"
    category_link = "small%20home%20appliances"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class ClimateEquipmentSpider(ProductsSpider):
    name = "climate-equipment-list"
    category_link = "climate%20equipment"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class KitchenAppliancesSpider(ProductsSpider):
    name = "kitchen-home-appl-list"
    category_link = "kitchen%20appliances"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class MemoryCardsSpider(ProductsSpider):
    name = "memory-cards-list"
    category_link = "memory%20cards"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class PortableSpeakersSpider(ProductsSpider):
    name = "portable-speakers-list"
    category_link = "portable%20speakers"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class PowerBanksSpider(ProductsSpider):
    name = "power-banks-list"
    category_link = "power%20banks"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class TiresSpider(ProductsSpider):
    name = "tires-list"
    category_link = "tires"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class WatchesSpider(ProductsSpider):
    name = "watches-list"
    category_link = "smart%20watches"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)


class WearablesSpider(ProductsSpider):
    name = "wearables-list"
    category_link = "wearables"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{PRODUCTS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category_link)
