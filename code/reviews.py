from scrapy.crawler import CrawlerProcess
from spiders import spider_reviews as reviews


def start():
    process = CrawlerProcess()
    # process.crawl(reviews.SmartphonesSpider)
    # process.crawl(reviews.PerfumesSpider)
    # process.crawl(reviews.BeautySpider)
    # process.crawl(reviews.BooksSpider)
    # process.crawl(reviews.CarAudioSpider)
    # process.crawl(reviews.CarElectronicsSpider)
    # process.crawl(reviews.HeadphonesSpider)
    # process.crawl(reviews.WatchesSpider)
    # process.crawl(reviews.WearablesSpider)
    # process.crawl(reviews.BigHomeAppSpider)
    # process.crawl(reviews.SmallHomeAppSpider)
    # process.crawl(reviews.ClimateEquipmentSpider)
    # process.crawl(reviews.KitchenHomeAppSpider)
    # process.crawl(reviews.MemoryCardsSpider)
    # process.crawl(reviews.PortableSpeakersSpider)
    # process.crawl(reviews.PowerBanksSpider)
    # process.crawl(reviews.TiresSpider)
    process.start()


if __name__ == '__main__':
    start()
