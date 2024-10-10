from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.article import Article
from app.main import app
from app.database.db import database

router = APIRouter()

articles_collection = database.get_collection("articles")

@app.post("/articles")
async def create_article(article: Article):
    article_dict = article.model_dump()
    article_dict['url'] = str(article_dict['url'])

    for image in article_dict['images']:
        image['url'] = str(image['url'])

    result = await articles_collection.insert_one(article_dict)
    return {"id": str(result.inserted_id), "message": "Article created successfully"}

@app.get("/articles")
async def get_all_articles():
    articles = []
    async for article in articles_collection.find():
        article["_id"] = str(article["_id"])  
        articles.append(article)
    return articles

@app.get("/articles/{article_id}")
async def get_article_by_id(article_id: str):
    try:
        article = await articles_collection.find_one({"_id": ObjectId(article_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article["_id"] = str(article["_id"])  
    return article
