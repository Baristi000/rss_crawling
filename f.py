import re, requests, json

def pare(data:str):
    data.replace("&","and")
    data = data.lower()
    data = re.sub(r"[^a-zA-Z0-9]+"," ",data)
    data = re.sub(r"\s","-",data)
    return data

def depare(data:str):
    data = data.replace("-"," ")
    return data

def faiss_train(data:list):
    response = requests.post(
        "http://tstsv.ddns.net:8000/edit/train/index_v1",
        data = json.dumps({
            "index": data
        })
    )
    print(response)
