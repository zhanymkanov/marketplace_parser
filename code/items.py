import scrapy


class Product(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    shopLink = scrapy.Field()
    brand = scrapy.Field()
    adjustedRating = scrapy.Field()
    reviewsQuantity = scrapy.Field()
    unitPrice = scrapy.Field()
    unitSalePrice = scrapy.Field()
    categoryID = scrapy.Field()
