import logging
import time

from app.utils import get_latest_date_in_dir

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
LOGGER = logging.getLogger()


def perf_logger(func):
    def wrapper(*args, **kwargs):
        LOGGER.info(f"Started {func.__name__}")
        start = time.perf_counter()
        func(*args, **kwargs)
        LOGGER.info(f"Finshed {func.__name__} in {time.perf_counter() - start}")

    return wrapper


def get_localized_latest_subdirectory(directory):
    localized = f"../{directory}"
    return get_latest_date_in_dir(localized)
