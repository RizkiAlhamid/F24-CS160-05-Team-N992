# This is where the on-demand article scrapping endpoint is defined
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.main import app
from app.database.db import database
from app.models.article import Article

router = APIRouter()


