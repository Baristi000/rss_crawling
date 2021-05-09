from fastapi import APIRouter
from . import crawling, search

api_router = APIRouter()

api_router.include_router(crawling.router,prefix='/Crawl',tags=['Crawling api'])
api_router.include_router(search.router,prefix='/Search',tags=['Search api'])