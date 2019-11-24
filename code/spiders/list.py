import scrapy
import json
from decouple import config


class ListSpider(scrapy.Spider):
    page = 1
    url = config('API_LIST_URL')
    referer_link = 'https://kaspi.kz/shop/c/{}/all/?page=1'

    headers = {"Accept": "application/json, text/*", "Accept-Encoding": "gzip, deflate, br",
               "Accept-Language": "ru,en;q=0.9,kk;q=0.8,es;q=0.7,ba;q=0.6", "Connection": "keep-alive",
               "Host": "kaspi.kz", "Referrer Policy": "no-referrer-when-downgrade",
               "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
               "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) "
                             "AppleWebKit/604.1.38 (KHTML, like Gecko) "
                             "Version/11.0 Mobile/15A372 Safari/604.1"}

    def __init__(self, category, limit=None):
        super().__init__()
        self.url = self.url.format(category=category, page='{}')
        self.headers['Referer'] = self.referer_link.format(category)
        self.limit = limit

    def start_requests(self):
        url = self.url.format(self.page)
        yield scrapy.Request(url, callback=self.parse_products,
                             headers=self.headers,
                             dont_filter=True)

    def parse_products(self, response):
        products = json.loads(response.text)
        for product in products['data']:
            yield {
                'id': product['id'],
                'title': product['title'],
                'shopLink': product['shopLink'],
                'brand': product['brand'],
                'adjustedRating': product['adjustedRating'],
                'reviewsQuantity': product['reviewsQuantity'],
                'unitPrice': product['unitPrice'],
                'unitSalePrice': product['unitSalePrice'],
                'categoryId': product['categoryId'],
            }

        if products['data']:
            if self.limit and self.page >= self.limit:
                return

            self.page += 1
            url = self.url.format(self.page)

            yield scrapy.Request(url=url,
                                 headers=self.headers,
                                 callback=self.parse_products,
                                 dont_filter=True)


class BeautyListSpider(ListSpider):
    name = 'beauty-list'
    category_link = 'beauty%20care%20equipment'

    def __init__(self):
        super().__init__(self.category_link)


class PerfumeListSpider(ListSpider):
    name = 'perfumes-list'
    category_link = 'perfumes'

    def __init__(self):
        super().__init__(self.category_link)


class BooksListSpider(ListSpider):
    name = 'books-list'
    category_link = 'books'

    def __init__(self):
        super().__init__(self.category_link)


class CarAudioListSpider(ListSpider):
    name = 'car-audio-list'
    category_link = 'car%20audio'

    def __init__(self):
        super().__init__(self.category_link)


class CarElectronicsListSpider(ListSpider):
    name = 'car-electronics-list'
    category_link = 'car%20electronics'

    def __init__(self):
        super().__init__(self.category_link)


class HeadphonesListSpider(ListSpider):
    name = 'headphones-list'
    category_link = 'headphones'

    def __init__(self):
        super().__init__(self.category_link)


class BigHomeAppliancesListSpider(ListSpider):
    name = 'big-home-appl-list'
    category_link = 'big%20home%20appliances'

    def __init__(self):
        super().__init__(self.category_link)


class SmallHomeAppliancesListSpider(ListSpider):
    name = 'small-home-appl-list'
    category_link = 'small%20home%20appliances'

    def __init__(self):
        super().__init__(self.category_link)


class ClimateEquipmentListSpider(ListSpider):
    name = 'climate-equipment-list'
    category_link = 'climate%20equipment'

    def __init__(self):
        super().__init__(self.category_link)


class KitchenAppliancesListSpider(ListSpider):
    name = 'kitchen-home-appl-list'
    category_link = 'kitchen%20appliances'

    def __init__(self):
        super().__init__(self.category_link)


class MemoryCardsListSpider(ListSpider):
    name = 'memory-cards-list'
    category_link = 'memory%20cards'

    def __init__(self):
        super().__init__(self.category_link)


class PortableSpeakersListSpider(ListSpider):
    name = 'portable-speakers-list'
    category_link = 'portable%20speakers'
    limit = 20

    def __init__(self):
        super().__init__(self.category_link, self.limit)


class PowerBanksListSpider(ListSpider):
    name = 'power-banks-list'
    category_link = 'power%20banks'

    def __init__(self):
        super().__init__(self.category_link)


class SmartphoneListSpider(ListSpider):
    name = 'smartphones-list'
    category_link = 'smartphones'

    def __init__(self):
        super().__init__(self.category_link)


class TiresListSpider(ListSpider):
    name = 'tires-list'
    category_link = 'tires'
    limit = 20

    def __init__(self):
        super().__init__(self.category_link, self.limit)


class WatchesListSpider(ListSpider):
    name = 'watches-list'
    category_link = 'smart%20watches'

    def __init__(self):
        super().__init__(self.category_link)


class WearablesListSpider(ListSpider):
    name = 'wearables-list'
    category_link = 'wearables'

    def __init__(self):
        super().__init__(self.category_link)
