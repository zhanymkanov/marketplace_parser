import json
import logging
import os
import time

from .exceptions import EmptyDirectoryException

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger()


def open_json(path):
    with open(path) as f:
        return json.load(f)


def get_latest_date_in_dir(dir):
    parse_dates = sorted(os.listdir(dir))
    parse_dates = filter_hidden_filenames(parse_dates)

    if not parse_dates:
        raise EmptyDirectoryException(
            f"No valid directories for parsing are found in {dir}"
        )

    return parse_dates[-1]


def filter_hidden_filenames(filenames):
    return [filename for filename in filenames if not filename.startswith(".")]


def perf_logger(func):
    def wrapper(*args, **kwargs):
        LOGGER.info(f"Started {func.__name__}")
        start = time.perf_counter()
        func(*args, **kwargs)
        LOGGER.info(f"Finshed {func.__name__} in {time.perf_counter() - start}")

    return wrapper
