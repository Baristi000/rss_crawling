from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
import uvicorn, traceback, os
from subprocess import run
from threading import Thread
from elasticsearch import Elasticsearch

from config import setting

app = FastAPI()
es = Elasticsearch([{'host':'tstsv.ddns.net','port':9200}])

@app.on_event("startup")
@repeat_every(seconds=60*60*8)
def crawl_all_exist_url():
    for url in list(setting.urls.keys()):
        crawl_one_url(url,True)

@app.get("/crawl_all_url")
def crawl_all(
    export_to_json:bool = False
):
    for url in list(setting.urls.keys()):
        crawl_one_url(url,export_to_json)
    return {"status":"success"}

@app.get("/crawl_one_url")
def crawing(
    url:str = None,
    export_to_json:bool = False
):
    return {"status":crawl_one_url(url,export_to_json)}

@app.get("/adding_url")
def add(
    url:str = None,
    crawl_type:str = "covid"
):
    setting.urls.update({url:crawl_type})
    setting.save()
    return {"status":"success"}

@app.get("/get_all_url")
def get_url():
    return{"url":list(setting.urls.keys())}

@app.get("/prune_null_data_file")
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

#crawl one url
def crawl_one_url(
    url:str = None,
    export:bool = False
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

@app.on_event("shutdown")
def a():
    print("done")

if __name__ == "__main__":
    uvicorn.run("api:app",host="0.0.0.0",port=8002, reload = True, timeout_keep_alive=5, backlog=80)