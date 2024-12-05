from pydantic import BaseModel
from typing import List, Dict, Optional

class Metadata(BaseModel):
    title: str
    author: Optional[str]
    publication_date: Optional[str]
    last_modified_date: Optional[str]
    tags: Optional[List[str]]
    categories: Optional[List[str]]

class Content(BaseModel):
    full_text: str
    paragraphs: List[str]
    word_count: int

class Analytics(BaseModel):
    reading_time_minutes: int

class Sentiment(BaseModel):
    overall: str
    tone: str
    emotional: str
    adjective: List[str]

class Article(BaseModel):
    url: str
    metadata: Metadata
    content: Content
    analytics: Optional[Analytics]
    environmental_keywords: Optional[Dict[str, int]]
    logline: str
    summary: str
    tags: List[str]
    main_topic: str
    key_points: List[str]
    sentiment: Sentiment
