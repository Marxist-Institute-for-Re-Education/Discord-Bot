import discord.ui as dc
from discord import Member, Guild, Role, PartialEmoji, Interaction, Object
from discord.channel import TextChannel
from discord.ext.commands import Context
from discord.ext.commands.errors import CheckFailure
from discord.ui import Modal
from discord.utils import get

from . import roles


__all__ = [
    "is_lit_chair",
    "require_role",
    "is_non_member"
    "require_non_member"
    "interacter_has_role",
    "get_role",
    "abbreviate",
    "ModalButton",
    "roles"
]


def is_lit_chair(value: Member | Interaction | Context) -> bool:
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

def require_non_member(user: Member) -> bool:
    if not is_non_member(user):
        raise CheckFailure(f"{user} is already a member")
    return True

def interacter_has_role(role: Object, name: str):
    async def check(interaction: Interaction) -> bool:
        return require_role(interaction.user, role, name)
    def decorator(cls: type[dc.Item | dc.View]):
        cls.interaction_check = check
        return cls
    return decorator

def get_role(guild: Guild, name: str) -> Role:
    role = get(guild.roles, name=name)

def abbreviate(s: str, length: int=100):
    if len(s) >= length:
        s = s[0:length - 4] + "..."
    return s


class Button(dc.Button):
    EMOJI: PartialEmoji

    def __init_subclass__(cls, *, emoji: str):
        cls.EMOJI = PartialEmoji.from_str(emoji)

    def __init__(self):
        super().__init__(emoji=self.EMOJI)


class ModalButton(dc.Button):
    EMOJI: PartialEmoji
    MODAL_CLASS: type[Modal]

    def __init_subclass__(cls, *, emoji: str, modal: type[Modal]):
        cls.EMOJI = PartialEmoji.from_str(emoji)
        cls.MODAL_CLASS = modal

    def __init__(self):
        super().__init__(emoji=self.EMOJI)

    async def callback(self, interaction: Interaction):
        interaction.response.send_modal(self.MODAL_CLASS())
