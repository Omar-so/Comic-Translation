import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .utils.cache import ImageCache
from .config import settings



from .routers.Auth.Auth import router as auth_router

from .routers.logic.router import router  as Logic_router

@asynccontextmanager
async def lifespan(app: FastAPI):


    
    ImageCache.connectAsync()


    yield

    
    await ImageCache.close()


app = FastAPI(lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router, tags=["Auth"])

app.include_router(Logic_router, tags=["Logic"])


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}