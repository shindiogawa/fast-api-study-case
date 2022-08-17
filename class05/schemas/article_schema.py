from re import L
from typing import Optional

from pydantic import BaseModel, HttpUrl


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    font_url: str
    description: str
    user_id: Optional[int]

    class Config:
        orm_mode = True
        
