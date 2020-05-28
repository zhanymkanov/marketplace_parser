import logging
from typing import List

from app import utils
from app.constants import DB_DUMPS_DIR, RATINGS_DIR
from app.db.session import LocalSession
from app.utils import load_json, perf_logger

LOGGER = logging.getLogger(__name__)

DB_DUMPS_DIR = f"../{DB_DUMPS_DIR}"
RATINGS_DIR = f"../{RATINGS_DIR}"


@perf_logger
def dump_into_tables():
    db = LocalSession()
    queries = db.insert_queries
    dumpfiles_with_queries = (
        ("categories.json", queries.bulk_insert_categories),
        ("products.json", queries.bulk_insert_products),
        ("reviews.json", queries.bulk_insert_reviews),
        ("specs.json", queries.bulk_insert_specs),
    )

    for source_file, query in dumpfiles_with_queries:
        _insert_from_source(source_file, query.sql)


@perf_logger
def dump_ratings_into_tables():
    cpu_columns = ("cpu", "rate", "versus")
    cpu_rating_files = ("laptop_cpus_versus.csv", "pc_cpus_versus.csv")

    gpu_columns = ("gpu", "rate", "versus")
    gpu_rating_files = ("laptop_gpus_versus.csv", "pc_gpus_versus.csv")

    _copy_rating_from_files(cpu_rating_files, "cpu_rating", cpu_columns)
    _copy_rating_from_files(gpu_rating_files, "gpu_rating", gpu_columns)


@perf_logger
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


@perf_logger
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


@perf_logger
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


@perf_logger
def create_views():
    db = LocalSession()
    queries = db.table_queries
    queries = [
        queries.create_view_notebooks.sql,
        queries.create_view_desktops.sql,
    ]

    for query in queries:
        db.exec_query(query)


@perf_logger
def _insert_from_source(source_file, query):
    db = LocalSession()
    date = utils.parse_latest_date(DB_DUMPS_DIR)

    data: List[dict] = load_json(f"{DB_DUMPS_DIR}/{date}/{source_file}")
    db.bulk_insert_dicts(query, data)


@perf_logger
def _copy_rating_from_files(files, table, columns):
    db = LocalSession()

    for file in files:
        with open(f"{RATINGS_DIR}/{file}") as f:
            db.copy_from(f, table, columns)


if __name__ == "__main__":
    drop_indexes()
    dump_into_tables()
    dump_ratings_into_tables()
    drop_duplicates()
    create_indexes()
    create_views()
