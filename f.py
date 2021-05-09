import re, requests, json
from config import setting
from encoder import UniversalEncoder

encoder = UniversalEncoder(setting.use_host,setting.use_port)

def pare(data:str):
    data.replace("&","and")
    data = data.lower()
    data = re.sub(r"[^a-zA-Z0-9]+"," ",data)
    data = data.strip()
    data = re.sub(r"\s+","-",data)
    return data

def depare(data:str):
    data = data.replace("-"," ")
    return data

def faiss_train(data:list):
    encoder.build_index(data,True)