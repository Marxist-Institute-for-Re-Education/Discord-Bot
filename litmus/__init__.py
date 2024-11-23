from discord import Message
from discord.ui import View
from discord.ext.commands import Context, Cog, command, Bot

from utils.channels import WELCOME
from logger import getLogger
from .elements import TakeLitmusButton


__all__ = [
    "LitmusTest",
    "setup",
    ]


logger = getLogger(__name__)


class LitmusTest(Cog, name = "Litmus Test"):
    UP_MESSAGE = "## Litmus Test\nInteract with the button below to submit your litmus test!"
    DOWN_MESSAGE = "## Litmus Test\nBot is currently down, please reach out to a CC member!"

    def __init__(self, bot: Bot):
        super().__init__()
        self.bot: Bot = bot
        self.is_connected: bool = True
        self.welcome_ch = bot.get_channel(WELCOME.id)
        self.message: Message = None

    @command(name="reset-litmus", help="Reset litmus message")
    async def reset_litmus(self, ctx: Context):
        await self.find_litmus_message()
        await ctx.message.add_reaction("✅")

    @Cog.listener("on_connect")
    async def on_connect(self):
        await self.send_up_message()
        self.is_connected = True

    @Cog.listener("on_disconnect")
    async def on_disconnect(self):
        if self.is_connected:
            await self.send_down_message()
        self.is_connected = False

    # provides an alternative to "reset-litmus"
    async def cog_load(self):
        if self.welcome_ch is None:
            self.welcome_ch = await self.bot.fetch_channel(WELCOME.id)
        await self.find_litmus_message()
        await self.send_up_message()
        return await super().cog_load()

    async def find_litmus_message(self) -> Message:
        logger.debug("finding litmus message")
        async for msg in self.welcome_ch.history(limit=5):
            if msg.content.find("## Litmus Test") != -1:
                logger.debug(f"found litmus message (ID:{msg.id})")
                self.message = msg
                break
        if self.message is None: # no message found
            logger.info("existing message not found; sending new litmus test message")
            self.message = await self.welcome_ch.send(
                self.UP_MESSAGE,
                view=self.view
                )
        return self.message

    @property
    def view(self) -> View:
        return View().add_item(TakeLitmusButton())

    async def send_up_message(self):
        logger.info("reset litmus buttons")
        await self.message.edit(content=self.UP_MESSAGE, view=self.view)

    async def send_down_message(self):
        logger.info("disabled litmus buttons")
        await self.message.edit(content=self.DOWN_MESSAGE)


async def setup(bot: Bot):
    await bot.add_cog(LitmusTest(bot))
