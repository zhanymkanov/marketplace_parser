from decouple import config

PRODUCTS_DIR = '../data/products'
REVIEWS_DIR = '../data/reviews'
REVIEWS_PER_REQUEST = 4000

HEADERS = {
    "Accept": "application/json, text/*", "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru,en;q=0.9,kk;q=0.8,es;q=0.7,ba;q=0.6", "Connection": "keep-alive",
    "Host": config('host'), "Cache-Control": "no-cache, no-store, max-age=0"
}
