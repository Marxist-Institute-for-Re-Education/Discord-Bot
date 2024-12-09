from discord import Object, Member, Guild, Role, PartialEmoji, Interaction
from discord.ext.commands import Context
from discord.ext.commands.errors import CheckFailure
from discord.utils import get

from .typing import Union


__all__ = [
    "CADRE",
    "CENTRAL_COMMITTEE",
    "BOOK_CLUB",
    "GENERAL_MEMBER",
    "is_lit_chair",
    "require_role",
    "is_non_member"
    "require_non_member"
    "interacter_has_role",
    "get_role",
]


CADRE: Object = Object(id=1294050744814801006)
CENTRAL_COMMITTEE: Object = Object(id=1294029964676436158)
BOOK_CLUB: Object = Object(id=1294040886203912262)
GENERAL_MEMBER: Object = Object(id=1306006885882794066)


def is_lit_chair(value: Union[Member, Interaction, Context]) -> bool:
    user: Member
    if isinstance(value, Member):
        user = value
    elif isinstance(value, Interaction):
        user = value.user
    else:
        user = value.author
    in_lit_com = get(user.roles, name="Literature Committee") is not None
    in_cc = get(user.roles, name="Central Committee") is not None
    return in_lit_com and in_cc

def require_role(user: Member, role: Object, name: str) -> bool:
    if user.get_role(role.id) is None:
        raise CheckFailure(f"{user} missing role: {name}")
    else:
        return True

def is_non_member(user: Member) -> bool:
    return len(user.roles) <= 1

def has_any_role(user: Member, *roles: Object) -> bool:
    for role in roles:
        if user.get_role(role) is not None:
            return True
    return False

def require_non_member(user: Member) -> bool:
    if not is_non_member(user):
        raise CheckFailure(f"{user} is already a member")
    return True

def get_role(guild: Guild, name: str) -> Role:
    role = get(guild.roles, name=name)
