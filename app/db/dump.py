import logging
from typing import List

from app import utils
from app.constants import DB_DUMPS_DIR, RATINGS_DIR
from app.db.session import LocalSession
from app.utils import load_json, perf_logger

LOGGER = logging.getLogger(__name__)

DB_DUMPS_DIR = f"../{DB_DUMPS_DIR}"
RATINGS_DIR = f"../{RATINGS_DIR}"


def dump_into_tables():
    db = LocalSession()
    queries = db.insert_queries

    source_files = (
        "categories.json",
        "products.json",
        "reviews.json",
        "computers-specs.json",
    )
    queries = (
        queries.bulk_insert_categories.sql,
        queries.bulk_insert_products.sql,
        queries.bulk_insert_reviews.sql,
        queries.bulk_insert_specs.sql,
    )

    for source_file, query in zip(source_files, queries):
        _insert_from_source(source_file, query)


def dump_into_product_details():
    db = LocalSession()

    queries = db.insert_queries
    query = queries.bulk_insert_product_details

    _insert_from_source('product_details.json', query.sql)


def dump_ratings_into_tables():
    cpu_columns = ("cpu", "rate", "versus")
    cpu_rating_files = ("laptop_cpus_versus.csv", "pc_cpus_versus.csv")

    gpu_columns = ("gpu", "rate", "versus")
    gpu_rating_files = ("laptop_gpus_versus.csv", "pc_gpus_versus.csv")

    _copy_rating_from_files(cpu_rating_files, cpu_columns)
    _copy_rating_from_files(gpu_rating_files, gpu_columns)


@perf_logger
def _insert_from_source(source_file, query):
    db = LocalSession()
    date = utils.parse_latest_date(DB_DUMPS_DIR)

    data: List[dict] = load_json(f"{DB_DUMPS_DIR}/{date}/{source_file}")
    db.bulk_insert_dicts(query, data)


@perf_logger
def _copy_rating_from_files(files, columns):
    db = LocalSession()

    for file in files:
        with open(f"{RATINGS_DIR}/{file}") as f:
            db.copy_from(f, "gpu_rating", columns)


def create_indexes():
    db = LocalSession()
    queries = db.create_index_queries

    queries = (
        queries.create_category_indexes,
        queries.create_product_indexes,
        queries.create_review_indexes,
        queries.create_specs_indexes,
        queries.create_cpu_rating_indexes,
        queries.create_gpu_rating_indexes,
    )

    for query in queries:
        db.exec_query(query.sql)


def drop_indexes():
    db = LocalSession()
    queries = db.drop_index_queries
    queries = (
        queries.drop_category_indexes,
        queries.drop_product_indexes,
        queries.drop_review_indexes,
        queries.drop_specs_indexes,
        queries.drop_cpu_rating_indexes,
        queries.drop_gpu_rating_indexes,
    )

    for query in queries:
        db.exec_query(query.sql)


def drop_duplicates():
    db = LocalSession()
    queries = db.drop_duplicates_queries
    queries = (
        queries.drop_product_duplicates,
        queries.drop_review_duplicates,
        queries.drop_category_duplicates,
        queries.drop_cpu_rating_duplicates,
        queries.drop_gpu_rating_duplicates,
    )

    for query in queries:
        db.exec_query(query.sql)


if __name__ == "__main__":
    drop_indexes()
    dump_into_tables()
    dump_into_product_details()
    dump_ratings_into_tables()
    drop_duplicates()
    create_indexes()
