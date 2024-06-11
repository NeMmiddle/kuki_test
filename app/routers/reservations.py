from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from ..dependencies import get_db
from datetime import date

router = APIRouter()


@router.post("/reserve/", response_model=schemas.Book)
def reserve_book(book_id: int, user_id: int, reservation_end_date: date, db: Session = Depends(get_db)):
    """
        Ручка для бронирования книги на временный промежуток конкретным пользователем.
    """
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    if db_book.reserved_by_user_id is not None:
        raise HTTPException(status_code=400, detail="Книга уже зарезервирована")
    db_book.reservation_end_date = reservation_end_date
    db_book.reserved_by_user_id = user_id
    db.commit()
    db.refresh(db_book)
    return db_book


@router.post("/release/", response_model=schemas.Book)
def release_book(book_id: int, db: Session = Depends(get_db)):
    """
        Ручка для сдачи книги, очистка поля бронирования в базе.
    """
    db_book = crud.get_book(db=db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    db_book.reservation_end_date = None
    db_book.reserved_by_user_id = None
    db.commit()
    db.refresh(db_book)
    return db_book
