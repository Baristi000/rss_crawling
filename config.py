import json
class Setting():
    config = json.load(open("./config.json"))
    urls:dict = config["urls"]
    elastic_host:str = config["elastic_host"]
    elastic_port:int = config["elastic_port"]
    def save(self):
        json.dump(self.config,open("./config.json","w"))

setting = Setting()