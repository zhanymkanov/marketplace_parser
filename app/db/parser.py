import json
import os
import re
import unicodedata
from datetime import date, datetime

import orjson

from app.constants import DB_DUMPS_DIR, PRODUCTS_DIR, REVIEWS_DIR, SPECS_DIR
from app.utils import filter_hidden_filenames, open_json

from .processing import processed_specs
from .utils import get_localized_latest_subdirectory, perf_logger

PRODUCTS_DIR = get_localized_latest_subdirectory(PRODUCTS_DIR)
REVIEWS_DIR = get_localized_latest_subdirectory(REVIEWS_DIR)
SPECS_DIR = get_localized_latest_subdirectory(SPECS_DIR)

DB_DUMPS_DIR = f"../{DB_DUMPS_DIR}/{date.today()}"
os.makedirs(DB_DUMPS_DIR, exist_ok=True)


@perf_logger
def parse_categories():
    categories = os.listdir(PRODUCTS_DIR)
    categories = filter_hidden_filenames(categories)

    categories_id_name = {}
    for category in categories:
        products = open_json(f"{PRODUCTS_DIR}/{category}")
        categories_id_name.update(
            {product["category_id"]: product["category_name"] for product in products}
        )

    categories_id_name = sorted(
        categories_id_name.items(), key=lambda id, name: (name, id)
    )

    categories = [{"source_id": id, "name": name} for id, name in categories_id_name]
    with open(f"{DB_DUMPS_DIR}/categories.json", "w") as f:
        json.dump(categories, f)


@perf_logger
def parse_products():
    categories = os.listdir(PRODUCTS_DIR)
    categories = filter_hidden_filenames(categories)

    products = []
    for category in categories:
        category_products = open_json(f"{PRODUCTS_DIR}/{category}")
        products.extend(category_products)

    with open(f"{DB_DUMPS_DIR}/products.json", "w") as f:
        f.write(json.dumps(products, ensure_ascii=False))


@perf_logger
def parse_reviews():
    categories = os.listdir(REVIEWS_DIR)
    categories = filter_hidden_filenames(categories)

    reviews = []
    for category in categories:
        products = os.listdir(f"{REVIEWS_DIR}/{category}")
        products = [p for p in products if not p.startswith(".")]

        for product in products:
            product_id = product[: product.index(".json")]
            product_reviews = open_json(f"{REVIEWS_DIR}/{category}/{product}")

            for review in product_reviews["data"]:
                review_rating = review["feedback"]["reviewsRating"]
                approved, rated = _parse_approved_rated(review_rating)
                reviews.append(
                    {
                        "product_id": product_id,
                        "source_id": review["id"],
                        "date": datetime.strptime(review["date"], "%d.%m.%Y"),
                        "rating": review["rating"],
                        "comment_plus": review["comment"]["plus"],
                        "comment_minus": review["comment"]["minus"],
                        "comment_text": review["comment"]["text"],
                        "review_approved": approved,
                        "review_rated": rated,
                    }
                )

    with open(f"{DB_DUMPS_DIR}/reviews.json", "wb") as f:
        f.write(orjson.dumps(reviews))


@perf_logger
def parse_specs():
    categories_with_specs = (
        "desktops",
        "notebooks",
    )

    specs = []
    for category in categories_with_specs:
        products = open_json(f"{SPECS_DIR}/{category}-specs.json")
        specs.extend([processed_specs(p) for p in products])

    with open(f"{DB_DUMPS_DIR}/specs.json", "w") as f:
        json.dump(specs, f, ensure_ascii=False)


def _parse_approved_rated(review_rating):
    if not review_rating:
        return None, None

    review_rating = unicodedata.normalize("NFKD", review_rating)
    match = re.search(r"(\d+\s*\d*)\s+из\s+(\d+\s*\d*)", review_rating)
    approved, rated = map(lambda x: int(x.replace(" ", "")), match.groups())
    return approved, rated


if __name__ == "__main__":
    parse_categories()
    parse_products()
    parse_reviews()
    parse_specs()
