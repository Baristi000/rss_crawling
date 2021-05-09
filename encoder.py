import numpy as np
import requests, faiss, os, json
from config import setting
import numpy as np
from db import crud, models
from db.database import engine, session

class UniversalEncoder():
        
    FEATURE_SIZE = 512
    BATCH_SIZE = 32
    vectors_dir = str(os.path.realpath("."))+"/search_data/faiss.index"

    def __init__(self, host, port):
        self.server_url = "http://{host}:{port}/v1/models/model:predict".format(
            host = host,
            port = port
        )
        try:
            setting.index_on_ram = faiss.read_index(self.vectors_dir)
        except Exception:
            setting.index_on_ram = None
        try:
            models.Base.metadata.create_all(bind=engine)
        except:
            pass
        self.session = session()

    @staticmethod
    def _standardized_input(sentence:str):
        return sentence.replace("\n", "").lower().strip()[:1000]

    def encode(self,data):
        data = [self._standardized_input(sentence=sentence) for sentence in data]
        all_vectors = []
        for i in range(0, len(data), self.BATCH_SIZE):
            batch = data[i:i+self.BATCH_SIZE]
            res = requests.post(
                url=self.server_url,
                json = {"instances":batch}
            )
            if not res.ok:
                print("FALSE")
            all_vectors += res.json()["predictions"]
        all_vectors = np.array(all_vectors,dtype="f")
        return all_vectors
    
    def build_index(self, datas:list, append:bool=True):
        data = []
        [data.append(d.replace("-"," ")) for d in datas]
        vector = self.encode(data)                                         #converter data to vectors
        if append == False or crud.get_all(self.session) == []:
            setting.index_on_ram = faiss.IndexFlatL2(self.FEATURE_SIZE)    #init the index
            crud.delete_all(self.session)
        #data process
        [crud.create_data(self.session,i) for i in data]
        setting.index_on_ram.add(vector)
        try:
            faiss.write_index(setting.index_on_ram,self.vectors_dir)
        except:
            os.mkdir(self.vectors_dir.split("/")[-2])
            f = open(self.vectors_dir,"w")
            f.close()
            faiss.write_index(setting.index_on_ram,self.vectors_dir)
        return setting.index_on_ram
    
    def search(self, query, numb_result:int=1):
        if setting.index_on_ram == None:
            setting.index_on_ram = faiss.read_index(self.vectors_dir)
        index = setting.index_on_ram
        query_vector = self.encode([query])
        top_k_result = index.search(query_vector, numb_result)
        [print(id) for id in top_k_result[1].tolist()[0]]
        return [
            crud.get_at(self.session,_id) for _id in top_k_result[1].tolist()[0]
        ]

    def remove_index(self, query):
        try:
            #get current indexs
            if setting.index_on_ram == None:
                setting.index_on_ram = faiss.read_index(self.vectors_dir)
            #search index
            query_vector = self.encode([query])
            id = setting.index_on_ram.search(query_vector,1)[1][0][0]
            #remove data from index and data on ram
            setting.index_on_ram.remove_ids(np.array([id]))
            crud.delete_at(self.session,id)
            #update data
            faiss.write_index(setting.index_on_ram,self.vectors_dir)
        except Exception:
            return False
        return True
