from enum import IntEnum
from typing import Optional
from typing_extensions import Self

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm.session import Session

from .base import *


class Status(IntEnum):
    Priority = 1
    Pending = 2
    Finished = 3

    def as_emoji(self) -> str:
        if self == Status.Priority:
            return "❗"
        elif self == Status.Pending:
            return "🔜"
        else: # self == Status.Finished:
            return "✅"


class Suggestion(Base):
    __tablename__ = "suggestions"

    title: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    next_ch: Mapped[Optional[int]] = mapped_column(default=0, name="next_chapter")
    total_ch: Mapped[int] = mapped_column(default=0, name="total_chapters")
    notes: Mapped[str] = mapped_column(nullable=False, default="")
    status: Mapped[Status] = mapped_column(nullable=False, default=Status.Pending)

    @classmethod
    def get(cls, title: str) -> Self:
        with Session(engine) as session:
            stmt = select(cls).where(cls.title == title)
            return session.scalar(stmt)

    @classmethod
    def from_user(cls, user_id: int) -> Self:
        with Session(engine) as session:
            stmt = select(cls).where(cls.user_id == user_id)
            return session.scalar(stmt)

    @classmethod
    def remove(cls, title: str):
        with Session(engine) as session:
            session.delete(cls.get(title))

    @classmethod
    def new(
        cls,
        title: str,
        user_id: int,
        total_ch: int = None,
        notes: str = None,
        status: Status = Status.Pending
    ):
        with new_session() as session:
            sug = cls(
                title=title,
                user_id=user_id,
                total_ch=total_ch,
                notes=notes,
                status=status
                )
            session.add(sug)

    def display_title(self) -> str:
        title = self.title
        if self.is_finished:
            title = f"~~{title}~~"
        emoji = self._status.as_emoji() + " "
        chapters: str = ""
        if self.is_chaptered:
            chapters = f" (ch. {self.next_ch} of {self.total_ch})"
        return emoji + title + chapters

    @property
    def is_chaptered(self) -> bool:
        return self.total_ch > 0

    @property
    def is_prioritized(self) -> bool:
        return self._status == Status.Priority
    @is_prioritized.setter
    def is_prioritized(self, value: bool):
        if self._status == Status.Finished:
            raise TypeError("Suggestion cannot change priority when active or finished")
        elif value:
            self._status = Status.Priority
        else:
            self._status = Status.Pending

    @property
    def is_finished(self) -> bool:
        if self.next_ch > self.total_ch:
            self._status = Status.Finished
            return True
        return self._status == Status.Finished
    def finish(self):
        self.next_ch = self.total_ch
        self.__status = Status.Finished
        self.TABLE.update(
            {
                "next_chapter": self.next_ch,
                "status": self._status
            },
            doc_ids=[self.doc_id]
        )


__all__ = [
    "Suggestion",
    "Status"
]
