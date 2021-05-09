from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from routers.api import api_router

#declare app
app = FastAPI()
#allow access on all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI()
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("api:app",host="0.0.0.0",port=8002, reload = True, timeout_keep_alive=5, backlog=80)