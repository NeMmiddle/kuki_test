from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

celery = Celery(__name__, broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task
def check_book_reservations():
    """
        При наступлении даты окончания бронирования снимает книгу с брони.
    """
    db: Session = SessionLocal()
    time_now = datetime.now()
    books = db.query(models.Book).filter(models.Book.reservation_end_date >= time_now).all()
    for book in books:
        book.reservation_end_date = None
        book.reserved_by_user_id = None
        db.commit()
    db.close()


# Раз в 30 секунд запускает функцию check_book_reservations.
celery.conf.beat_schedule = {
    'check-book-reservations-every-day': {
        'task': 'app.tasks.check_book_reservations',
        'schedule': 30.0,
    },
}
celery.conf.timezone = 'Europe/Moscow'