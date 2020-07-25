from datetime import date

import scrapy
from decouple import config

from app.constants import SPECS_DIR
from app.utils import open_json, parse_latest_date


class SpecsSpider(scrapy.Spider):
    referer_link = config("referer_link")

    def __init__(self, category):
        super().__init__()
        self.products_json = self._get_category_products(category)

    def start_requests(self):
        products = open_json(self.products_json)
        for product in products:
            yield scrapy.Request(
                url=product["url"],
                cb_kwargs={"product": product},
                callback=self.parse_product,
            )

    def parse_product(self, response, product):
        """
        Parse product specs

        dl - is the block
        dt - is the header
        dd - is the body

        dd may be the root of other dls
        """
        details = {}
        blocks = response.xpath('//dl[contains(@class,"specifications-list__spec")]')
        for block in blocks:
            characteristic = block.xpath("dt/span/text()").get()
            value = block.xpath("dd/text()").get()

            details[characteristic] = value

        yield {
            "source_id": product["source_id"],
            "title": product["title"],
            "url": product["url"],
            "brand": product["brand"],
            "rating": product["rating"],
            "reviews_quantity": product["reviews_quantity"],
            "price_unit": product["price_unit"],
            "price_sale": product["price_sale"],
            "category_id": product["category_id"],
            "category_name": product["category_name"],
            "parsed_details": details,
        }

    @staticmethod
    def _get_category_products(category):
        latest_date = parse_latest_date(SPECS_DIR)
        category_products = f"{SPECS_DIR}/{latest_date}/{category}-list.json"
        return category_products


class SmartphoneSpecsSpider(SpecsSpider):
    name = "smartphones-specs"
    category = "smartphones"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{SPECS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category)


class NotebooksSpecsSpider(SpecsSpider):
    name = "notebooks-specs"
    category = "notebooks"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{SPECS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category)


class DesktopsSpecsSpider(SpecsSpider):
    name = "desktops-specs"
    category = "desktops"
    custom_settings = {
        "FEED_FORMAT": "json",
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_URI": f"{SPECS_DIR}/{date.today()}/{name}.json",
    }

    def __init__(self):
        super().__init__(self.category)
