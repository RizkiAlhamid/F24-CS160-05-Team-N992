# This is where the on-demand article scrapping endpoint is defined
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.main import app
from app.database.db import database
from app.models.article import Article
from kubernetes import client, config

router = APIRouter(prefix="/webscraper")


@router.post("/scrape_bbc_article")
def scrape_bbc_article(url: str):
    """
    Create a Kubernetes Job to scrape the article from the given URL
    """
    # TODO:



@router.get("/scrape_bbc")
def scrape_bbc():
    """
    Create a Kubenertes CronJob to scrape the latest articles from BBC
    """
    # TODO:


