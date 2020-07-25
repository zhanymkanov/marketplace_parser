import json
import os
import re
import unicodedata
from datetime import date, datetime

import orjson

from app.constants import DB_DUMPS_DIR, PRODUCTS_DIR, REVIEWS_DIR, SPECS_DIR
from app.db.processing import processed_specs
from app.utils import open_json, get_latest_date_in_dir, filter_hidden_filenames
from app.db.utils import perf_logger

PRODUCTS_DIR = f"../{PRODUCTS_DIR}"
REVIEWS_DIR = f"../{REVIEWS_DIR}"
SPECS_DIR = f"../{SPECS_DIR}"

DB_DUMPS_DIR = f"../{DB_DUMPS_DIR}/{date.today()}"
os.makedirs(DB_DUMPS_DIR, exist_ok=True)


@perf_logger
def parse_categories():
    latest_parse_date = _get_latest_parse_date()
    categories = _get_categories(latest_parse_date)

    categories_id_name = _parse_categories_id_name(categories, latest_parse_date)
    _save_categories_for_dump(categories_id_name)


@perf_logger
def parse_products():
    date_latest = get_latest_date_in_dir(PRODUCTS_DIR)
    products_latest = f"{PRODUCTS_DIR}/{date_latest}"

    categories = os.listdir(products_latest)
    categories = [c for c in categories if not c.startswith(".")]
    categories_with_specs = (
        "desktops",
        "notebooks",
    )

    products, products_with_specs = [], set()
    for category in categories_with_specs:
        category_products = open_json(f"{SPECS_DIR}/{date_latest}/{category}-list.json")
        products_with_specs.update({p["source_id"] for p in category_products})
        products.extend(category_products)

    for category in categories:
        category_products = open_json(f"{products_latest}/{category}")
        category_products = [
            p for p in category_products if p["source_id"] not in products_with_specs
        ]
        products.extend(category_products)

    with open(f"{DB_DUMPS_DIR}/products.json", "w") as f:
        f.write(json.dumps(products, ensure_ascii=False))


@perf_logger
def parse_reviews():
    date_latest = get_latest_date_in_dir(REVIEWS_DIR)
    reviews_latest = f"{REVIEWS_DIR}/{date_latest}"

    categories = os.listdir(reviews_latest)
    categories = [c for c in categories if not c.startswith(".")]

    reviews = []
    for category in categories:
        products = os.listdir(f"{reviews_latest}/{category}")
        products = [p for p in products if not p.startswith(".")]

        for product in products:
            product_id = product[: product.index(".json")]
            product_reviews = open_json(f"{reviews_latest}/{category}/{product}")

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
    date_latest = get_latest_date_in_dir(SPECS_DIR)
    categories_with_specs = (
        "desktops",
        "notebooks",
    )

    specs = []
    for category in categories_with_specs:
        products = open_json(f"{SPECS_DIR}/{date_latest}/{category}-specs.json")
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


def _get_latest_parse_date():
    date_latest = get_latest_date_in_dir(f"{PRODUCTS_DIR}")
    return f"{PRODUCTS_DIR}/{date_latest}"


def _get_categories(parse_date):
    categories = os.listdir(parse_date)
    return filter_hidden_filenames(categories)


def _parse_categories_id_name(categories, latest_parse_date):
    categories_id_name = {}
    for category in categories:
        products = open_json(f"{latest_parse_date}/{category}")
        categories_id_name.update({
            product["category_id"]: product["category_name"] for product in products
        })

    return sorted(categories_id_name.items(), key=lambda id, name: (name, id))


def _save_categories_for_dump(categories_id_name):
    categories = [{"source_id": id, "name": name} for id, name in categories_id_name]
    with open(f"{DB_DUMPS_DIR}/categories.json", "w") as f:
        json.dump(categories, f)


if __name__ == "__main__":
    parse_categories()
    parse_products()
    parse_reviews()
    parse_specs()
