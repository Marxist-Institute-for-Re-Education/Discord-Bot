from discord import Intents
from discord.ext.commands import Bot, Context
from discord.ext.commands.errors import ExtensionError


bot = Bot(
    command_prefix = "/",
    intents = Intents.all(),
    )

EXTENSIONS: list[str] = [
    # "book_club",
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
    exts = list(bot.extensions)
    for ext in exts:
        await bot.reload_extension(ext)
    print("~~~~~ reloading ~~~~~")
    await ctx.message.delete()

@bot.command(name="add-ext", hidden=True)
async def add_extension(ctx: Context, name: str):
    try:
        await bot.load_extension(name)
    except ExtensionError as err:
        await ctx.send(f"Failed to load {name}")
        raise err
    else:
        await ctx.send(f"Added {name}")

__all__ = ["bot"]
