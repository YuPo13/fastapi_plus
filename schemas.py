from pydantic import BaseModel

class AuthorCreate(BaseModel):
    name: str
    surname: str
    country: str

class BookCreate(BaseModel):
    title: str
    author_id: int
    published_year: int
