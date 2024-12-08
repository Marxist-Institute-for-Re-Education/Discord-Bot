from discord import Guild, ScheduledEvent, EventStatus
from discord.ui import View
from discord.ext.commands import Context, Cog, command, Bot

from utils.roles import get, is_lit_chair
from logger import getLogger
from bot import MireBot
from .suggestions import *


__all__ = [
    "BookClub",
    "setup"
]


logger = getLogger(__name__)


class BookClub(Cog, name = "Book Club"):
    """Everything related to Book Club!"""

    def __init__(self, bot: MireBot):
        self.bot = bot
        super().__init__()

    @command(help="View the current Book Club book suggestion list")
    async def suggestions(self, ctx: Context):
        logger.debug("(command) listing suggestions")
        embed = suggestions_embed()
        view = View()
        view.add_item(AddButton())
        view.add_item(RemoveButton())
        view.add_item(EditButton())
        if not is_lit_chair(ctx.author):
            view.add_item(PrioritizeButton())
        return await ctx.send(embed=embed, view=view)

    async def cog_check(self, ctx: Context) -> bool:
        return get(ctx.author.roles, name="Book Club") is not None

async def setup(bot: Bot):
    await bot.add_cog(BookClub(bot))
