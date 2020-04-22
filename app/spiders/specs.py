from datetime import date

import scrapy
from decouple import config

from app.constants import SPECS_DIR
from app.db import utils as db_utils
from app.utils import load_json, parse_latest_date


class SpecsSpider(scrapy.Spider):
    referer_link = config("referer_link")

    def __init__(self, category):
        super().__init__()
        parse_date = parse_latest_date(SPECS_DIR)
        self.products_json = f"{SPECS_DIR}/{parse_date}/{category}-list.json"

    def start_requests(self):
        parsed_ids = db_utils.get_dumped_product_details()
        products = load_json(self.products_json)

        for product in products:
            if product["source_id"] in parsed_ids:
                continue

            yield scrapy.Request(
                url=product["url"],
                cb_kwargs={"product": product},
                callback=self.parse_product,
            )
            parsed_ids.add(product["source_id"])

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
