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
        indexs = Selector(response).xpath("//*[name() = \"item\"]").xpath("//*[name()=\"title\"]/text()").extract()
        links = Selector(response).xpath("//*[name() = \"item\"]").xpath("//*[name()=\"link\"]/text()").extract()
        descriptions = Selector(response).xpath("//*[name() = \"item\"]").xpath("//*[name()=\"description\"]/text()").extract()
        pubDates = Selector(response).xpath("//*[name() = \"item\"]").xpath("//*[name()=\"pubDate\"]/text()").extract()
        trainable = []
        for i in range(len(indexs)):
            indexs[i] = pare(indexs[i])
            print(indexs[i])
            print(links[i])
            print(pubDates[i])
            print(descriptions[i])
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
                faiss_train(str(depare(index)))
            except ElasticsearchException as err:
                pass