from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.models.article import Article
from app.models.persona import Personas
from app.main import app
from app.database.db import database

router = APIRouter()

articles_collection = database.get_collection("articles")

# For posting one article
@router.post("/article") 
async def create_article(article: Article):
    article_dict = article.model_dump()

    result = await articles_collection.insert_one(article_dict)
    return {"id": str(result.inserted_id), "message": "Article summary posted successfully"}

@router.get("/articles")
async def get_all_articles():
    articles = []
    async for article in articles_collection.find():
        article["_id"] = str(article["_id"])  
        articles.append(article)
    return articles

@router.get("/articles/{article_id}")
async def get_article_by_id(article_id: str):
    try:
        # Find using Mongo's '_id'
        if ObjectId.is_valid(article_id):
            article = await articles_collection.find_one({"_id": ObjectId(article_id)})
        # Find using custom 'CID'
        else:
            article = await articles_collection.find_one({"CID": article_id})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Convert '_id' to string for JSON serialization
    article["_id"] = str(article["_id"])
    return article
