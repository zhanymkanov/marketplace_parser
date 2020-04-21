import logging
from typing import List

import anosql
import psycopg2
import psycopg2.extras
from decouple import config

from app.constants import SQL_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger(__name__)


class Base:
    def __init__(self):
        self.conn = psycopg2.connect(config("DATABASE_URL"))

    def _exec_query(self, query):
        try:
            with self.conn as c:
                cur = c.cursor()
                cur.execute(query)
        except psycopg2.Error as exc:
            LOGGER.error(exc)

    def _fetch_one(self, query):
        try:
            with self.conn as c:
                cur = c.cursor()
                cur.execute(query)
                return cur.fetchone()
        except psycopg2.Error as exc:
            LOGGER.error(exc)

    def _fetch_all(self, query):
        try:
            with self.conn as c:
                cur = c.cursor()
                cur.execute(query)
                return cur.fetchall()
        except psycopg2.Error as exc:
            LOGGER.error(exc)

    def _exec_with_tuples(self, query, values: List):
        try:
            with self.conn as c:
                cur = c.cursor()
                psycopg2.extras.execute_values(cur, query, values)
        except psycopg2.Error as exc:
            LOGGER.error(exc)

    def _exec_with_dicts(self, query, values: List[dict]):
        try:
            with self.conn as c:
                cur = c.cursor()
                psycopg2.extras.execute_batch(cur, query, values)
        except psycopg2.Error as exc:
            LOGGER.error(exc)

    def _copy_from(self, file, table, columns, sep=","):
        try:
            with self.conn as c:
                cur = c.cursor()
                cur.copy_from(file, table, sep=sep, columns=columns)
        except psycopg2.Error as exc:
            LOGGER.error(exc)


class LocalSession(Base):
    def __init__(self):
        super().__init__()
        self.create_tables()

    def create_tables(self):
        queries = self.table_queries
        queries = [
            queries.create_category.sql,
            queries.create_product.sql,
            queries.create_specs.sql,
            queries.create_review.sql,
            queries.create_gpu_rating.sql,
            queries.create_cpu_rating.sql,
        ]

        for query in queries:
            self._exec_query(query)

    @property
    def table_queries(self):
        return anosql.from_path(f"{SQL_DIR}/create_tables.sql", "psycopg2")

    @property
    def insert_queries(self):
        return anosql.from_path(f"{SQL_DIR}/insert_values.sql", "psycopg2")

    @property
    def create_index_queries(self):
        return anosql.from_path(f"{SQL_DIR}/create_indexes.sql", "psycopg2")

    @property
    def drop_index_queries(self):
        return anosql.from_path(f"{SQL_DIR}/drop_indexes.sql", "psycopg2")

    @property
    def drop_duplicates_queries(self):
        return anosql.from_path(f"{SQL_DIR}/drop_duplicates.sql", "psycopg2")

    def exec_query(self, query):
        self._exec_query(query)

    def select_one(self, query):
        return self._fetch_one(query)

    def select_all(self, query):
        return self._fetch_all(query)

    def bulk_insert_tuples(self, query, data: List):
        self._exec_with_tuples(query, data)

    def bulk_insert_dicts(self, query, data: List[dict]):
        self._exec_with_dicts(query, data)

    def copy_from(self, file, table, columns, sep=","):
        self._copy_from(file, table, columns, sep)
