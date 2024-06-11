from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Date, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class BookGenre(Base):
    __tablename__ = "book_genres"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    pages = Column(Integer)
    author_id = Column(Integer, ForeignKey("users.id"))
    reservation_end_date = Column(DateTime, nullable=True)
    reserved_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    author = relationship("User", foreign_keys=[author_id])
    reserved_by = relationship("User", foreign_keys=[reserved_by_user_id])
    genres = relationship("Genre", secondary="book_genres", back_populates="books")


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    avatar = Column(String)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("Book", secondary="book_genres", back_populates="genres")
