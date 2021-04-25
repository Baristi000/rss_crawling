import scrapy, re
from scrapy.selector import Selector
from elasticsearch import Elasticsearch
from config import setting

es = Elasticsearch([{'host':setting.elastic_host,'port':setting.elastic_port}])

class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        indexs = Selector(response).xpath("/rss/channel/item/title/text()").extract()
        links = Selector(response).xpath("/rss/channel/item/link/text()").extract()
        descriptions = Selector(response).xpath("/rss/channel/item/description/text()").extract()
        pubDates= Selector(response).xpath("/rss/channel/item/pubDate/text()").extract()
        for i in range(len(indexs)):
            indexs[i].replace("&","and")
            indexs[i] = re.sub(r"[^a-zA-Z0-9]+"," ",indexs[i])
            body = {
                "description":descriptions[i],
                "pubDate":pubDates[i],
                "crawl_url":self.start_urls[0]
            }
            index = indexs[i]
            print(index)
            print(index)
            print(index)
            es.index(index = index, body=body)
        print("***************************************")
        print(indexs[0])
        print(links[0])
        print(descriptions[0])
        print(pubDates[0])
        print("***************************************")
