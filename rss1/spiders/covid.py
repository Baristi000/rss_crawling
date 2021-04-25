import scrapy, re
from scrapy.selector import Selector
from elasticsearch import Elasticsearch
from config import setting
from f import pare

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
            indexs[i] = pare(indexs[i])
            print(indexs[i])
            body = {
                "description":descriptions[i],
                "pubDate":pubDates[i],
                "crawl_url":self.start_urls[0]
            }
            index = indexs[i]
            es.index(index = index, body=body)
