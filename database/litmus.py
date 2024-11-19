from typing import Optional
from typing_extensions import Self

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.session import Session

from .base import *


__all__ = [
    "LitmusTest",
    "get_litmus_msg",
    "set_litmus_msg",
    "LitmusTestMessage"
]


class LitmusTest(Base):
    __tablename__ = "litmus_tests"

    user: Mapped[int] = mapped_column(primary_key=True)
    tendency: Mapped[str]
    pali_solution: Mapped[str]
    organizations: Mapped[str]
    why: Mapped[str]
    how: Mapped[str]

    @classmethod
    def get(cls, user_id: int) -> Self:
        with new_session() as session:
            query = select(LitmusTest).where(cls.user == user_id)
            return session.scalar(query)


class LitmusTestMessage(Base):
    __tablename__ = "litmus_message"

    message_id: Mapped[int] = mapped_column(primary_key=True)

def get_litmus_msg() -> int:
    with new_session() as session:
        result = session.scalar(select(LitmusTestMessage))
        return result.message_id

def set_litmus_msg(id: int):
    with new_session() as session:
        result = session.scalar(select(LitmusTestMessage))
        result.message_id = id
        session.commit()
