from fastapi import APIRouter
from fastapi_utils.tasks import repeat_every
from subprocess import run
import traceback, os
from config import setting
import time

router = APIRouter()

def crawl_one_url(
    url:str = None,
    export:bool = True
):
    try:
        crawl_type = setting.urls[url]
        if export:
            run(["python","crawl.py",f"{url}",f"{crawl_type}","json"])
        else:
            run(["python","crawl.py",f"{url}",f"{crawl_type}"])
    except Exception:
        traceback.print_exc()
        return False
    return True

@router.get("/crawl_all_url")
def crawl_all(
    export:bool = True
):
    start_time=time.time()
    for url in list(setting.urls.keys()):
        crawl_one_url(url,export)
    return {"time consuming":time.time()-start_time}

@router.get("/crawl_one_url")
def crawing(
    url:str = None,
    export:bool = True #export to json
):
    start_time=time.time()
    crawl_one_url(url,export)
    return {"time consuming":time.time()-start_time}

@router.get("/adding_url")
def add(
    url:str = None,
    crawl_type:str = "covid"
):
    setting.urls.update({url:crawl_type})
    setting.save()
    return {"status":"success"}

@router.get("/get_all_url")
def get_url():
    return{"url":list(setting.urls.keys())}

@router.get("/prune_null_data_file")
#check and delete all null data file in DataStore directory
def prune():
    origin_path = str(os.path.realpath("."))+"/DataStore/"
    dirs = os.listdir(origin_path)
    result = {}
    size = 0.0
    for path in dirs:
        result.update({origin_path+path:os.stat(origin_path+path).st_size})
        size+=os.stat(origin_path+path).st_size
        if os.stat(origin_path+path).st_size == 0:
            os.remove(origin_path+path)
    return {
        "total_size":str(size*.1/1024/1024)+" mb",
        "detail":result
    }

@router.on_event("startup")
@repeat_every(seconds=60*60*8)
def crawl_all_exist_url():
    for url in list(setting.urls.keys()):
        crawl_one_url(url,True)