import logging
import os
from datetime import date

from .exceptions import EmptyDirectoryException

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()


def get_parse_date(dir):
    parse_date = date.today()

    if not os.path.exists(f'{dir}/{parse_date}'):
        LOGGER.warning(f'Products for {parse_date} are not parsed and collected yet')
        parse_date = _get_latest_date_in_dir(dir)

    LOGGER.info(f'Reviews from {parse_date} are being parsed')

    return parse_date


def _get_latest_date_in_dir(dir):
    parse_dates = sorted(os.listdir(dir))
    parse_dates = [parse_date for parse_date in parse_dates if not parse_date.startswith('.')]

    if not parse_dates:
        raise EmptyDirectoryException(f"No valid directories for parsing are found in {dir}")

    return parse_dates[-1]
