import time

from app.utils import LOGGER


def perf_logger(func):
    def wrapper(*args, **kwargs):
        LOGGER.info(f"Started {func.__name__}")
        start = time.perf_counter()
        func(*args, **kwargs)
        LOGGER.info(f"Finshed {func.__name__} in {time.perf_counter() - start}")

    return wrapper
