import json
import os
import re
import unicodedata
from datetime import date, datetime

import orjson

from app import utils
from app.constants import DB_DUMPS_DIR, PRODUCTS_DIR, REVIEWS_DIR, SPECS_DIR
from app.db.processing import processed_specs
from app.utils import load_json, perf_logger

PRODUCTS_DIR = f"../{PRODUCTS_DIR}"
REVIEWS_DIR = f"../{REVIEWS_DIR}"
SPECS_DIR = f"../{SPECS_DIR}"

DB_DUMPS_DIR = f"../{DB_DUMPS_DIR}/{date.today()}"
os.makedirs(DB_DUMPS_DIR, exist_ok=True)


@perf_logger
def parse_categories():
    date_latest = utils.parse_latest_date(f"{PRODUCTS_DIR}")
    products_latest = f"{PRODUCTS_DIR}/{date_latest}"

    categories = os.listdir(products_latest)
    categories = [c for c in categories if not c.startswith(".")]
    computer_subcategories = (
        "desktops",
        "notebooks",
    )

    categories_set, categories_with_specs = set(), {}

    # Desktops and Notebooks categories inherit from Computers,
    # so they might have IDs intersection
    for category in computer_subcategories:
        category_products = load_json(f"{SPECS_DIR}/{date_latest}/{category}-list.json")
        categories_with_specs.update(
            {p["category_id"]: category for p in category_products}
        )

    for category in categories:
        products = load_json(f"{products_latest}/{category}")
        for product in products:
            if product["category_id"] in categories_with_specs:
                name = categories_with_specs[product["category_id"]]
            else:
                name = product["category_name"].replace("%20", " ")

            categories_set.add((name, product["category_id"]))

    categories_sorted = sorted(categories_set, key=lambda x: (x[0], x[1]))
    categories_dict = [{"name": c[0], "source_id": c[1]} for c in categories_sorted]

    with open(f"{DB_DUMPS_DIR}/categories.json", "w") as f:
        json.dump(categories_dict, f)


@perf_logger
def parse_products():
    date_latest = utils.parse_latest_date(PRODUCTS_DIR)
    products_latest = f"{PRODUCTS_DIR}/{date_latest}"

    categories = os.listdir(products_latest)
    categories = [c for c in categories if not c.startswith(".")]
    categories_with_specs = (
        "desktops",
        "notebooks",
    )

    products, products_with_specs = [], set()
    for category in categories_with_specs:
        category_products = load_json(f"{SPECS_DIR}/{date_latest}/{category}-list.json")
        products_with_specs.update({p["source_id"] for p in category_products})
        products.extend(category_products)

    for category in categories:
        category_products = load_json(f"{products_latest}/{category}")
        category_products = [
            p for p in category_products if p["source_id"] not in products_with_specs
        ]
        products.extend(category_products)

    with open(f"{DB_DUMPS_DIR}/products.json", "w") as f:
        f.write(json.dumps(products, ensure_ascii=False))


@perf_logger
def parse_reviews():
    date_latest = utils.parse_latest_date(REVIEWS_DIR)
    reviews_latest = f"{REVIEWS_DIR}/{date_latest}"

    categories = os.listdir(reviews_latest)
    categories = [c for c in categories if not c.startswith(".")]

    reviews = []
    for category in categories:
        products = os.listdir(f"{reviews_latest}/{category}")
        products = [p for p in products if not p.startswith(".")]

        for product in products:
            product_id = product[: product.index(".json")]
            product_reviews = load_json(f"{reviews_latest}/{category}/{product}")

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
    date_latest = utils.parse_latest_date(SPECS_DIR)
    categories_with_specs = (
        "desktops",
        "notebooks",
    )

    specs = []
    for category in categories_with_specs:
        products = load_json(f"{SPECS_DIR}/{date_latest}/{category}-specs.json")
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
