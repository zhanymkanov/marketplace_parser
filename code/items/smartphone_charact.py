import scrapy

class Smartphone_charact(scrapy.Item):
    type = scrapy.Field()
    standard = scrapy.Field()
    os = scrapy.Field()
    sim = scrapy.Field()
    color = scrapy.Field(serializer=str)