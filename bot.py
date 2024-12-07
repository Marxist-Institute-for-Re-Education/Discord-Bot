from discord import Intents, Guild, User
from discord.ext.commands import Bot, Context, command, dm_only
from discord.ext.commands.errors import ExtensionError

from utils.typing import List
from logger import getLogger


__all__ = [
    "MireBot",
]


logger = getLogger(__name__)


class MireBot(Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "!",
            intents = Intents(
                emojis = True,
                guild_polls = True,
                guild_reactions = True,
                guild_scheduled_events = True,
                guilds = True,
                invites = True,
                members = True,
                message_content = True,
                messages = True,
                moderation = True,
                # manage_events = True,
                ),
            description = "Commands and events for MIRE"
        )
        self.debug_users: List[User] = []

    async def setup_hook(self):
        for ext in self.get_extensions_list():
            await self.load_extension(ext)
        return await super().setup_hook()

    async def load_extension(self, name):
        logger.debug(f"loading extension {name}")
        return await super().load_extension(name)

    @command(name="reload", hidden=True)
    async def reload(self, ctx: Context):
        for ext in self.get_extensions_list():
            await self.reload_extension(ext)
        await ctx.message.add_reaction("✅")

    @command(name="add-ext", hidden=True)
    async def add_extension(self, ctx: Context, name: str):
        try:
            await self.load_extension(name)
            open(self.FILENAME, mode="a").write(name)
        except ExtensionError as err:
            await ctx.send(f"Failed to load {name}")
            raise err
        else:
            await ctx.send(f"Added {name}")

    @property
    def guild(self) -> Guild:
        return self.guilds[0]

    @staticmethod
    def get_extensions_list() -> List[str]:
        lines = open("extensions.txt", mode="r").readlines()
        return [line.strip() for line in lines]
