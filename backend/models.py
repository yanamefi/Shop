from pydantic import BaseModel


class Products(BaseModel):
    id: int
    post_date: str
    name: str
    photo: str
    description: str

