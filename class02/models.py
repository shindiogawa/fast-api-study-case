from curses.ascii import islower
from multiprocessing.sharedctypes import Value
from typing import Optional

from pydantic import BaseModel, validator

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    classes: int
    hours: int

    @validator('title')
    def validate_title(cls, value: str):
        words = value.split(' ')
        if len(words) < 3:
            raise ValueError('The title should have at least 3 characters')
        if value.islower():
            raise ValueError('The title should be capitalized')        
        return value

courses = [
    Course(id=1, title = 'Programming for Dummies', classes= 42, hours = 24),
    Course(id=2, title = 'Programming in Java', classes= 32, hours = 14),
    Course(id=3, title = 'Programming in Python', classes= 12, hours = 64),
]


