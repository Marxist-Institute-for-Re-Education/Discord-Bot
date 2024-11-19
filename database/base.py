import os
from abc import abstractmethod
from typing_extensions import Self

from sqlalchemy import select, create_engine, URL, Engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import DeclarativeBase

from dotenv import load_dotenv

__all__ = [
    "Base",
    "engine",
    "new_session"
]


class Base(DeclarativeBase):
    @classmethod
    def all(cls) -> list[Self]:
        with Session(engine) as session:
            return session.scalars(select(cls)).all()

    @classmethod
    @abstractmethod
    def get(cls, value) -> Self:
        ...


load_dotenv()

_HOST = os.getenv("DATABASE_HOST")
_USERNAME = os.getenv("DATABASE_USERNAME")
_PASSWORD = os.getenv("DATABASE_PASSWORD")
_DB_NAME = os.getenv("DATABASE_NAME")
_URL = URL.create(
    "mysql",
    username = _USERNAME,
    password = _PASSWORD,
    host = _HOST,
    database = _DB_NAME
)
print("~~~~~~~~~~~~~~~~~~~\n DEBUG:", _URL, "\n~~~~~~~~~~~~~~")
engine: Engine = create_engine(_URL)


def new_session() -> Session:
    return Session(engine)
