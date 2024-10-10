from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hi, welcome to the webscraper!"}

from app.routers.webscraper import *

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8081)
