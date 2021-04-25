from scrapy.crawler import CrawlerProcess
from rss1.spiders.covid import CovidSpider
import sys

if __name__ == "__main__":
    url = str(sys.argv[1])
    process = CrawlerProcess()
    process.crawl(CovidSpider,start_urls=[url],kwargs={
        "allowed_domains":[url.split("/")[2].split(":")[0]]
        })
    process.start()