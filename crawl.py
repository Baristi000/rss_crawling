from scrapy.crawler import CrawlerProcess
from rss1.spiders import covid#, covid2
import sys
from config import setting

if __name__ == "__main__":
    url = str(sys.argv[1])
    process = CrawlerProcess()

    if setting.urls[url] == "covid":
        process.crawl(covid.CovidSpider,start_urls=[url],kwargs={
            "allowed_domains":[url.split("/")[2].split(":")[0]]
            })
    #another case
    ''' elif setting.urls[url] == "covid2":
        process.crawl(covid2.Covid2Spider,start_urls=[url],kwargs={
            "allowed_domains":[url.split("/")[2].split(":")[0]]
            }) '''
    
    process.start()