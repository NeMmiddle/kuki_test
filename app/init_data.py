from sqlalchemy.orm import Session

from app import models


def init_db(db: Session) -> None:
    """
    Заполнение базы тестовыми данными если они пустые.
    """
    if db.query(models.Genre).count() == 0:
        genres = [
            models.Genre(name="Фантастика"),
            models.Genre(name="Научпоп"),
            models.Genre(name="Роман"),
        ]
        for genre in genres:
            db.add(genre)

    if db.query(models.Genre).count() == 0:
        users = [
            models.User(first_name="Миша", last_name="Иванов", avatar=""),
            models.User(first_name="Игорь", last_name="Игоревич", avatar=""),
            models.User(first_name="Айн", last_name="Рэнд", avatar=""),
        ]
        for user in users:
            db.add(user)

    db.commit()
