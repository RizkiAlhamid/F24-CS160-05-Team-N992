# This is where the on-demand article scrapping endpoint is defined
from fastapi import APIRouter, HTTPException
from app.models.article import Article
from kubernetes import client, config
from app.lib.scrapings.bbc.scraper import DATA_PATH, bbc_scraper
from app.lib.scrapings.bbc.transform import filter_environmental_articles
from app.lib.llm.article_summarizer import summarize_articles
from pathlib import Path
from pydantic import BaseModel
from app.lib.personas.persona import get_first_persona 


router = APIRouter(prefix="/webscraper")


@router.post("/scrape_bbc_article")
async def scrape_bbc_article(url: str):
    """
    Create a Kubernetes Job to scrape the article from the given URL
    """
    # TODO:

class ScrapeRequest(BaseModel):
    url: str
    pages_count: int


@router.post("/scrape_bbc")
async def scrape_bbc(request: ScrapeRequest):
    """
    Create a Kubernetes CronJob to scrape the latest articles from BBC.
    """
    try:
        # Call the scraper function
        scraped_articles_path = bbc_scraper(request.url, request.pages_count, None)
        DATA_PATH = Path("./data")
        filtered_articles_path = DATA_PATH / "environmental_articles.json"
        filter_environmental_articles(scraped_articles_path, filtered_articles_path)

        persona = await get_first_persona()
        if not persona:
            raise HTTPException(status_code=404, detail="No personas found in the database.")

        await summarize_articles(filtered_articles_path, persona)

        return {"message": "Scraping & summarizing completed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

