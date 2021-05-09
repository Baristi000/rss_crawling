from fastapi import APIRouter, Body, HTTPException
from config import setting
from db import crud
from encoder import UniversalEncoder
import time

router = APIRouter()
encoder = UniversalEncoder(setting.use_host,setting.use_port)

@router.post("/search/{DATA}")
def search(
    data: str= Body(...,embed=True),
    nums_of_result:int = Body(1,embed=True)
):
    try:
        return encoder.search(data,nums_of_result)
    except:
        return None

@router.get("/reset")
def reset():
    start_time = time.time()
    raw_data = setting.es.indices.get_alias("*")
    datas = list(raw_data.keys())
    encoder.build_index(datas,False)
    return {"time consuming":time.time()-start_time}

@router.get("/delete_all")
def delete_all():
    datas = setting.es.indices.get_alias("*")
    try:
        [setting.es.indices.delete(index=data, ignore=[400, 404]) for data in datas]
    except:
        pass