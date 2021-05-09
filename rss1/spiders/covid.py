import scrapy, re
from scrapy.selector import Selector
from elasticsearch import Elasticsearch, ElasticsearchException
from config import setting
from f import pare, faiss_train, depare
import uuid
import time
from rss1.items import Rss1Item

es = Elasticsearch([{'host':setting.elastic_host,'port':setting.elastic_port}])

class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = [url.split("/")[2].split(":")[0] for url in list(setting.urls.keys())]
    start_urls = list(setting.urls.keys())
    custom_settings = {
        'LOG_ENABLED': True,
        'LOG_LEVEL'  : "WARNING"
    }

    def parse(self, response):
        indexs = Selector(response).xpath("//*[name() = \"item\"]")[0].xpath("//*[name()=\"title\"]/text()").extract()
        links = Selector(response).xpath("//*[name() = \"item\"]")[0].xpath("//*[name()=\"link\"]/text()").extract()
        descriptions = Selector(response).xpath("//*[name() = \"item\"]")[0].xpath("//*[name()=\"description\"]/text()").extract()
        pubDates = Selector(response).xpath("//*[name() = \"item\"]")[0].xpath("//*[name()=\"pubDate\"]/text()").extract()
        if len(pubDates) == 0:
            pubDates = Selector(response).xpath("//*[name() = \"item\"]")[0].xpath("//*[name()=\"pubdate\"]/text()").extract()
        train_index = []
        print("*******************************************")
        print(self.start_urls)
        print(len(indexs))
        for i in range(len(indexs)):
            indexs[i] = pare(indexs[i])
            body = {}
            #update description
            try:
                body.update({"description":descriptions[i]})
            except:
                body.update({"description":"not provided"})
            
            #update pubDate
            try:
                body.update({"pubDate":pubDates[i]})
            except:
                named_tuple = time.localtime() # get struct_time
                time_string = time.strftime("%m/%d/%Y", named_tuple)
                body.update({"pubDate":time_string})
            id = uuid.uuid4()
            index = indexs[i]

            #update crawl_url
            body.update({"crawl_url":self.start_urls[0]})

            #update link
            try:
                body.update({"link":links[i]})
            except:
                body.update({"link":"not provided"})

            #try to put data to elastisearch, train search data, yield data to json file
            try:
                #insert into eplastic search server
                es.indices.create(index=index)      
                r = es.index(index=index,body=body,doc_type='{}'.format(index), ignore=400)
                #send trian data
                train_index.append(str(depare(index)))
                # yield data to json file
                item = Rss1Item()
                item["index"] = index
                item["description"] = index
                item["pubDate"] = index
                item["link"] = index
                item["crawl_url"] = index
                yield item
            except ElasticsearchException as err:
                pass
        if train_index != []:
            faiss_train(train_index)