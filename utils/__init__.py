import typing as ty
import discord.ui as dc
from discord import Member, Guild, Role, Interaction, Object
from discord.ext.commands import Context
from discord.ext.commands.errors import CheckFailure
from discord.utils import get

from . import roles
from . import channels
from . import typing


__all__ = [
    # Modules
    "roles",
    "channels",
    "typing",
    # Other
    "abbreviate",
    "Button",
    "ModalButton",
]

class classproperty(object):
    def __init__(self, getter: ty.Callable[[ty.Any], ty.Any]):
        self.getter: ty.Callable[[ty.Any], ty.Any] = getter

    def __get__(self, obj, cls):
        return self.f(cls)

def abbreviate(s: str, length: int=100):
    if len(s) >= length:
        s = s[0:length - 4] + "..."
    return s
