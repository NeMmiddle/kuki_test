from typing import Optional, Type, List

from sqlalchemy.orm import Session
from .. import models, schemas


def get_genre(db: Session, genre_id: int) -> Optional[models.Genre]:
    """
       Получает Жанр из базы данных по её id.
    """
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def get_genres(db: Session, skip: int = 0, limit: int = 10) -> List[Type[models.Genre]]:
    """
       Получает жанры из базы данных по фильтрам.
    """
    return db.query(models.Genre).offset(skip).limit(limit).all()


def create_genre(db: Session, genre: schemas.GenreCreate) -> Optional[models.Genre]:
    """
       Создае жанр в базе данных.
    """
    db_genre = models.Genre(
        title=genre.name,
    )
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def update_genre(db: Session, genre_id: int, genre: schemas.GenreUpdate) -> Optional[models.Genre]:
    """
       Обновляет информацию о жанре в базе данных.
    """
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not db_genre:
        return None
    for key, value in genre.dict(exclude_unset=True).items():
        setattr(db_genre, key, value)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def delete_genre(db: Session, genre_id: int) -> Optional[models.Genre]:
    """
       Удаляет жанр из базы данных.
    """
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if not db_genre:
        return None
    db.delete(db_genre)
    db.commit()
    return db_genre
