from app.utils import get_latest_date_in_dir


def get_localized_latest_subdirectory(directory):
    localized = f"../{directory}"
    return get_latest_date_in_dir(localized)
