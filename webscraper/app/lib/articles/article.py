from app.database.db import database
from app.lib.logging import logging
from app.models.article import Article

collection = database.articles

async def save_article_to_db(article: Article):
    article_dict = article.model_dump()
    url = article_dict.get("url")

    if not url:
        logging.error("URL is required for creating an article.")
        return {"error": "URL is required for creating an article"}

    result = await collection.replace_one(
        {"url": url},  # Query to check for existing article with the same URL
        article_dict,  # New data to replace with
        upsert=True    # Insert the article if it doesn't exist
    )

    message = (
        "Article updated successfully"
        if result.matched_count > 0
        else "Article created successfully"
    )
    return {"id": str(result.upserted_id or result.matched_count), "message": message}
