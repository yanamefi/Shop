# models.py

from datetime import datetime
from pydantic import BaseModel
from typing import List

class Products(BaseModel):
    id: int
    post_date: datetime
    pr_name: str
    photo: str
    description: str
    price: float
    photo_name: str
