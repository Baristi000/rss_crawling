import json
from elasticsearch import Elasticsearch

class Setting():
    config = json.load(open("./urls.json"))
    urls:dict = config["urls"]

    elastic_host:str = "tstsv.ddns.net"
    elastic_port:int = 9200
    db_host:str = "tstsv.ddns.net"
    use_host:str = "tstsv.ddns.net"
    use_port:int = 8501

    es = Elasticsearch([{'host':elastic_host,'port':elastic_port}])
    index_on_ram = None
    def save(self):
        json.dump(self.config,open("./urls.json","w"))

setting = Setting()