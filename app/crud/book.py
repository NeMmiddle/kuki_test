from typing import Optional, List, Type

from sqlalchemy.orm import Session
from .. import models, schemas
from ..models import Book


def get_book(db: Session, book_id: int) -> Optional[models.Book]:
    """
       Получает книгу из базы данных по её id.
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[Type[Book]]:
    """
       Получает книги из базы данных по фильтрам.
    """
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """
       Создает книгу в базе данных.
    """
    db_book = models.Book(
        title=book.title,
        price=book.price,
        pages=book.pages,
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    for genre_id in book.genres:
        db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
        db_book.genres.append(db_genre)
    db.commit()
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate) -> Optional[models.Book]:
    """
       Обновляет информацию о книге в базе данных.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Optional[models.Book]:
    """
       Удаляет книгу из базы данных.
    """
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book
