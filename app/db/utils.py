from app.db.session import LocalSession


def get_dumped_products():
    db_session = LocalSession()
    fetch_all = db_session.select_all("SELECT source_id FROM product")
    return {x[0] for x in fetch_all}


def get_dumped_specs_products():
    db_session = LocalSession()
    fetch_all = db_session.select_all("SELECT product_id FROM specs")
    return {x[0] for x in fetch_all}
