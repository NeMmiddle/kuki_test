from typing import List, Optional
from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    first_name: str
    last_name: str


class UserCreate(UserBase):
    avatar: Optional[str] = None


class UserUpdate(UserBase):
    avatar: Optional[str] = None


class User(UserBase):
    id: int
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    price: float
    pages: int
    author_id: int


class BookCreate(BookBase):
    genres: List[int]


class BookUpdate(BookBase):
    genres: List[int]


class Book(BookBase):
    id: int
    genres: List[Genre] = []

    class Config:
        from_attributes = True
