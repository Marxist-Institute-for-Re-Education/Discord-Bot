from .base import new_session, Base, engine
from .suggestion import Suggestion, Status

__all__ = [
    "Suggestion",
    "Status",
    "new_session",
    "LitmusTest",
]


Base.metadata.create_all(engine)
