# This is where the on-demand article scrapping endpoint is defined
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.db import database
from app.models.article import Article
from kubernetes import client, config
from app.lib.scrapings.bbc.scraper import DATA_PATH, bbc_scraper
from app.lib.scrapings.bbc.transform import filter_environmental_articles
from pathlib import Path
from pydantic import BaseModel

router = APIRouter(prefix="/webscraper")


@router.post("/scrape_bbc_article")
def scrape_bbc_article(url: str):
    """
    Create a Kubernetes Job to scrape the article from the given URL
    """
    # TODO:

class ScrapeRequest(BaseModel):
    url: str

@router.post("/scrape_bbc")
def scrape_bbc(request: ScrapeRequest):
    """
    Create a Kubernetes CronJob to scrape the latest articles from BBC.
    """
    try:
        # Call the scraper function
        scraped_articles_path = bbc_scraper(request.url, 5, None)
        DATA_PATH = Path("./data")
        output_file = DATA_PATH / "environmental_articles.json"
        filter_environmental_articles(scraped_articles_path, output_file)
        
        return {"message": "Scraping completed successfully.", "output_file": str(output_file)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
     



