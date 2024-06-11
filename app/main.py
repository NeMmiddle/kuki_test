from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from .routers import books, users, genres, reservations
from .database import engine, SessionLocal
from . import models
from .init_data import init_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    init_db(db)
    db.close()


app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")