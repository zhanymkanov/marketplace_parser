from scrapy.crawler import CrawlerProcess
from spiders import product_details


def start():
    process = CrawlerProcess()
    process.crawl(product_details.SmartphoneCharactSpider)
    # process.crawl(product_detailsPerfumeSpider)
    # process.crawl(product_detailsBeautySpider)
    # process.crawl(product_detailsBooksSpider)
    # process.crawl(product_detailsCarAudioSpider)
    # process.crawl(product_detailsCarElectronicsSpider)
    # process.crawl(product_detailsHeadphonesSpider)
    # process.crawl(product_detailsWatchesSpider)
    # process.crawl(product_detailsWearablesSpider)
    # process.crawl(product_detailsBigHomeAppliancesSpider)
    # process.crawl(product_detailsSmallHomeAppliancesSpider)
    # process.crawl(product_detailsClimateEquipmentSpider)
    # process.crawl(product_detailsKitchenAppliancesSpider)
    # process.crawl(product_detailsMemoryCardsSpider)
    # process.crawl(product_detailsPortableSpeakersSpider)
    # process.crawl(product_detailsPowerBanksSpider)
    # process.crawl(product_detailsTiresSpider)
    process.start()


if __name__ == '__main__':
    start()
