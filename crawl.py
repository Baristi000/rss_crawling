from scrapy.crawler import CrawlerProcess
from rss1.spiders import covid#, covid2
import sys, uuid, os
from config import setting

if __name__ == "__main__":

    if not os.path.exists('DataStore'):
        os.makedirs('DataStore')

    url = str(sys.argv[1])
    process = CrawlerProcess()
    if sys.argv[-1] == "json":
        process = CrawlerProcess({
            'FEED_FORMAT': 'json',
            'FEED_URI': str(os.path.realpath("."))+'/DataStore/'+str(uuid.uuid4())+".json"
        })

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