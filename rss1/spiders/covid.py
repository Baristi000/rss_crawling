import scrapy, re
from scrapy.selector import Selector
from elasticsearch import Elasticsearch, ElasticsearchException
from config import setting
from f import pare, faiss_train, depare
import uuid

es = Elasticsearch([{'host':setting.elastic_host,'port':setting.elastic_port}])

class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = []
    start_urls = []

    def parse(self, response):
        indexs = Selector(response).xpath("/rss/channel/item/title/text()").extract()
        #
        trainable = []
        links = Selector(response).xpath("/rss/channel/item/link/text()").extract()
        descriptions = Selector(response).xpath("/rss/channel/item/description/text()").extract()
        pubDates= Selector(response).xpath("/rss/channel/item/pubDate/text()").extract()
        #id = uuid.uuid4()
        #id = "e722a9e8-13c1-4868-a836-1ed8de72a4bd"
        for i in range(len(indexs)):
            indexs[i] = pare(indexs[i])
            print(indexs[i])
            body = {
                "description":descriptions[i],
                "pubDate":pubDates[i],
                "crawl_url":self.start_urls[0],
                "link":links[i]
            }
            id = uuid.uuid4()
            index = indexs[i]


            try:
                es.indices.create(index=index)                       #insert into eplastic search server
                es.index(index=index,body=body,doc_type='{}'.format(index))
                trainable.append(index)
            except ElasticsearchException as err:
                pass
        train_index = []
        for index in trainable:
            train_index.append(depare(index))
        faiss_train(train_index)