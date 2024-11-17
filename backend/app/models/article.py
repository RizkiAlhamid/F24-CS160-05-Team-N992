from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

# class Content(BaseModel):
#     paragraphs: List[str]

# class Image(BaseModel):
#     url: HttpUrl
#     alt: Optional[str]

# class Metadata(BaseModel):
#     category: Optional[str]
#     tags: List[str]
#     word_count: int
#     reading_time: str

# class Article(BaseModel):
#     title: str
#     url: HttpUrl
#     author: Optional[str]
#     published_date: Optional[str]
#     content: Content
#     metadata: Metadata
#     images: List[Image]
#     comments: List[str] = []

class Sentiment(BaseModel):
    overall: str
    tone: str
    emotional: str
    adjective: List[str]

class Video(BaseModel):
    CID: str
    channel: str
    vid: str
    title: str
    published_at: str
    transcript: str
    logline: str
    summary: str
    tags: List[str]
    main_topic: str
    key_points: List[str]
    sentiment: Sentiment

class Article(BaseModel):
    CID: str
    channel: str
    description: str
    subscriber_count: str
    video_count: str
    view_count: str
    videos: List[Video]
    main_topic: Optional[str] = None
    key_points: Optional[List[str]] = None
    sentiment: Optional[Sentiment] = None
