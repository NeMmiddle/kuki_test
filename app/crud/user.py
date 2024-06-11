from typing import Optional, Type, List

from sqlalchemy.orm import Session
from .. import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 10) -> Optional[models.User]:
    """
       Получает пользователя из базы данных по её id.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int) -> List[Type[models.User]]:
    """
       Получает пользователя из базы данных по фильтрам.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate, avatar_path: str = None) -> Optional[models.User]:
    """
       Создае пользователя в базе данных.
    """
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        avatar=avatar_path
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserUpdate) -> Optional[models.User]:
    """
       Обновляет информацию о пользователе в базе данных.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        if user.avatar:
            db_user.avatar = user.avatar
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[models.User]:
    """
       Удаляет пользователя из базы данных.
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
