from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..dependencies import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@router.get("{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book


@router.get("/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@router.delete("/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return db_book


@router.get("/filter", response_model=List[schemas.Book])
def filter_books(
    author_id: Optional[int] = None,
    genre_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    if genre_id:
        query = query.join(models.Book.genres).filter(models.Genre.id == genre_id)
    if min_price:
        query = query.filter(models.Book.price >= min_price)
    if max_price:
        query = query.filter(models.Book.price <= max_price)
    return query.all()