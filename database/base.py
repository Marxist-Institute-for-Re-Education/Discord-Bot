from abc import abstractmethod
from typing_extensions import Self

from sqlalchemy import select, create_engine
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    @classmethod
    def all(cls) -> list[Self]:
        with Session(engine) as session:
            return session.scalars(select(cls)).all()

    @classmethod
    @abstractmethod
    def get(cls, value) -> Self:
        ...
        # raise NotImplementedError(f"{repr(cls)}.get")


engine = create_engine("sqlite:///database.db")


def new_session() -> Session:
    return Session(engine)
