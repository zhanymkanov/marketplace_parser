from scrapy.crawler import CrawlerProcess
from spiders import list


def start_crawling():
    process = CrawlerProcess()
    process.crawl(list.SmartphonesSpider)
    process.crawl(list.PerfumeSpider)
    process.crawl(list.BeautySpider)
    process.crawl(list.BooksSpider)
    process.crawl(list.CarAudioSpider)
    process.crawl(list.CarElectronicsSpider)
    process.crawl(list.HeadphonesSpider)
    process.crawl(list.WatchesSpider)
    process.crawl(list.WearablesSpider)
    process.crawl(list.BigHomeAppliancesSpider)
    process.crawl(list.SmallHomeAppliancesSpider)
    process.crawl(list.ClimateEquipmentSpider)
    process.crawl(list.KitchenAppliancesSpider)
    process.crawl(list.MemoryCardsSpider)
    process.crawl(list.PortableSpeakersSpider)
    process.crawl(list.PowerBanksSpider)
    process.crawl(list.TiresSpider)
    process.start()


if __name__ == '__main__':
    start_crawling()
