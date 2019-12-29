import logging
import os

from .exceptions import EmptyDirectoryException

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def get_parse_date(dir, date):
    parse_date = date

    if not os.path.exists(f'{dir}/{parse_date}'):
        parse_date = _get_latest_date_in_dir(dir)
        LOGGER.warning(f'Products for {date} are not yet parsed and collected, {parse_date} is being used')

    return parse_date


def _get_latest_date_in_dir(dir):
    collection_dates = sorted(os.listdir(dir))
    collection_dates = [date for date in collection_dates if not date.startswith('.')]

    if not collection_dates:
        raise EmptyDirectoryException(f"No valid directories for parsing are found in {dir}")

    return collection_dates[-1]
