from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
from app.database.db import check_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup tasks here
    await check_connection()
    
    yield  # The application runs during this period
    
    # Perform shutdown tasks here (if any)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hi, welcome to the backend!"}

from app.routers.users import *
from app.routers.articles import *
from app.routers.articles import router as articles_router
from app.routers.personas import router as personas_router

app.include_router(articles_router)
app.include_router(personas_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
