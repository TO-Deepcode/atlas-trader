# Pydantic modelleri
from pydantic import BaseModel
from typing import Optional

class LogCreate(BaseModel):
    level: str
    message: str

class Log(LogCreate):
    id: int
    timestamp: str

class News(BaseModel):
    title: str
    url: str
    sentiment: Optional[str]
    published_at: str

class NewsStored(News):
    id: int
