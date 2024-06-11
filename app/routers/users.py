from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from .. import models, schemas, crud
from ..dependencies import get_db

router = APIRouter()

UPLOAD_DIRECTORY = "./uploads/avatars/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post("/", response_model=schemas.User)
def create_user(
        first_name: str,
        last_name: str,
        avatar: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    avatar_path = None
    if avatar:
        if avatar.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Допустимые фформаты файла jpg или png")

        avatar_path = os.path.join(UPLOAD_DIRECTORY, avatar.filename)

        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)

        if os.path.getsize(avatar_path) > 5 * 1024 * 1024:  # Проверка размера файла
            os.remove(avatar_path)
            raise HTTPException(status_code=400, detail="Размер аватара должен быть меньше 5 МБ.")

    return crud.create_user(db=db, user=schemas.UserCreate(first_name=first_name, last_name=last_name),
                            avatar_path=avatar_path)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        user_id: int,
        first_name: str,
        last_name: str,
        avatar: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    avatar_path = None
    if avatar:
        if avatar.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Допустимые фформаты файла jpg или png")

        avatar_path = os.path.join(UPLOAD_DIRECTORY, avatar.filename)

        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)

        if os.path.getsize(avatar_path) > 5 * 1024 * 1024:  # Проверка размера файла
            os.remove(avatar_path)
            raise HTTPException(status_code=400, detail="Размер аватара должен быть меньше 5 МБ.")

    user_data = schemas.UserUpdate(first_name=first_name, last_name=last_name, avatar=avatar_path)
    return crud.update_user(db=db, user_id=user_id, user=user_data)


@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user
