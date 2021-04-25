import re

def pare(data:str):
    data.replace("&","and")
    data = data.lower()
    data = re.sub(r"[^a-zA-Z0-9]+"," ",data)
    data = re.sub(r"\s","-",data)
    return data