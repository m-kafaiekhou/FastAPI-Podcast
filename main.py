from functools import lru_cache
from fastapi import FastAPI
import uvicorn
from api.v1 import podcast, interactions

from config.settings import settings


app = FastAPI()

app.include_router(podcast.router, prefix='/api')
app.include_router(interactions.router, prefix='/api')



if __name__ == "__main__":
    uvicorn.run("__main__:app", host="0.0.0.0", port=8002, log_level="debug", reload=True)
