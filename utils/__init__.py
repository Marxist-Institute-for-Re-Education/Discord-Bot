from typing import Type, Union

import discord.ui as dc
from discord import Member, Guild, Role, Interaction, Object
from discord.ext.commands import Context
from discord.ext.commands.errors import CheckFailure
from discord.utils import get

from . import roles
from . import channels
from . import types
from . import ui


__all__ = [
    "is_lit_chair",
    "require_role",
    "is_non_member",
    "interacter_has_role",
    "get_role",
    "has_any_role"
    "abbreviate",
    "channels",
    "roles",
    "types",
    "Button",
    "ModalButton",
]


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

def interacter_has_role(role: Object, name: str):
    async def check(interaction: Interaction) -> bool:
        return require_role(interaction.user, role, name)
    def decorator(cls: Type[dc.Item | dc.View]):
        cls.interaction_check = check
        return cls
    return decorator

def get_role(guild: Guild, name: str) -> Role:
    role = get(guild.roles, name=name)

def abbreviate(s: str, length: int=100):
    if len(s) >= length:
        s = s[0:length - 4] + "..."
    return s
