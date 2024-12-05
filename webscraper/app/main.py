from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.database.db import check_connection
from app.routers import webscraper

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup tasks here
    await check_connection()
    
    yield  # The application runs during this period
    
    # Perform shutdown tasks here (if any)

app = FastAPI(lifespan=lifespan)

app.include_router(webscraper.router)

@app.get("/")
def read_root():
    return {"message": "Hi, welcome to the webscraper!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081)
