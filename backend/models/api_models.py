from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    question: str
    source_ids: Optional[List[str]] = None
    top_k: int = 5


class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]] = []


class TextSourceRequest(BaseModel):
    title: str
    text: str


class YouTubeSourceRequest(BaseModel):
    title: str
    url: str