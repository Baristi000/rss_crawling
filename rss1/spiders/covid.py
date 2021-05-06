import scrapy, re
from scrapy.selector import Selector
from elasticsearch import Elasticsearch, ElasticsearchException
from config import setting
from f import pare, faiss_train, depare
import uuid
import time

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
        train_index = []
        print("*******************************************")
        print(len(indexs))
        for i in range(len(indexs)):
            indexs[i] = pare(indexs[i])
            try:
                body = {
                    "description":descriptions[i],
                    "pubDate":pubDates[i],
                    "crawl_url":self.start_urls[0],
                    "link":links[i]
                }
            except:
                named_tuple = time.localtime() # get struct_time
                time_string = time.strftime("%m/%d/%Y", named_tuple)
                body = {
                    "description":descriptions[i],
                    "pubDate":time_string,
                    "crawl_url":self.start_urls[0],
                    "link":links[i]
                }
            id = uuid.uuid4()
            index = indexs[i]

            
            try:
                es.indices.create(index=index)                       #insert into eplastic search server
                r = es.index(index=index,body=body,doc_type='{}'.format(index), ignore=400)
                trainable.append(index)
                train_index.append(str(depare(index)))
                faiss_train([str(depare(index))])
            except ElasticsearchException as err:
                break
        #faiss_train(train_index)