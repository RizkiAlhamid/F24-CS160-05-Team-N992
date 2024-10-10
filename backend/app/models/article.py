from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class Content(BaseModel):
    paragraphs: List[str]

class Image(BaseModel):
    url: HttpUrl
    alt: Optional[str]

class Metadata(BaseModel):
    category: Optional[str]
    tags: List[str]
    word_count: int
    reading_time: str

class Article(BaseModel):
    title: str
    url: HttpUrl
    author: Optional[str]
    published_date: Optional[str]
    content: Content
    metadata: Metadata
    images: List[Image]
    comments: List[str] = []