from scrapy.crawler import CrawlerProcess
from spiders import spider_details


def start():
    process = CrawlerProcess()
    process.crawl(spider_details.SmartphoneDetailsSpider)
    process.crawl(spider_details.ComputerDetailsSpider)
    process.start()


if __name__ == '__main__':
    start()
