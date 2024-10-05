from fastapi import FastAPI
import uvicorn
from app.routers import article_routes

app = FastAPI()
app.include_router(article_routes.router)

@app.get("/")
def read_root():
    return {"message": "Hi, welcome to the backend!"}

from app.routers.users import *

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
