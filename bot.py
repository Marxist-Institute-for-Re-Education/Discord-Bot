from discord import Intents
from discord.ext.commands import Bot, Context
from discord.ext.commands.errors import ExtensionError

from logger import getLogger


__all__ = [
    "bot",
    "setup_hook",
    ]


logger = getLogger(__name__)

bot = Bot(
    command_prefix = "/",
    intents = Intents.all(),
    )

EXTENSIONS: list[str] = [
    "book_club",
    "committee",
    "democracy",
    "litmus"
]

async def setup_hook():
    for ext in EXTENSIONS:
        await bot.load_extension(ext)
bot.setup_hook = setup_hook

@bot.command(name="reload", hidden=True)
async def reload(ctx: Context):
    logger.info("reloading extensions")
    exts = list(bot.extensions)
    for ext in exts:
        logger.debug(f"reloading {ext}")
        await bot.reload_extension(ext)
    await ctx.message.add_reaction("✅")

@bot.command(name="add-ext", hidden=True)
async def add_extension(ctx: Context, name: str):
    logger.info(f"adding extension ({name})")
    try:
        await bot.load_extension(name)
    except ExtensionError as err:
        logger.error("failed to load extension ({name})")
        await ctx.send(f"Failed to load extension: {name}")
        raise err
    else:
        await ctx.send(f"Added {name}")
