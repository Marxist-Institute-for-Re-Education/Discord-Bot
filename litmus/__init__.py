from discord import Message, TextChannel, PartialMessage
from discord.ui import View, Button
from discord.ext.commands import Context, Cog, command, Bot

from database import get_litmus_msg, set_litmus_msg
from utils.channels import WELCOME
from .elements import TakeLitmusButton


class LitmusTest(Cog, name = "Litmus Test"):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot: Bot = bot
        self.is_connected: bool = True
        self.welcome_ch = bot.get_channel(WELCOME.id)
        self._message: Message = None

    @Cog.listener("on_connect")
    async def on_connect(self):
        await self.send_up_message()
        self.is_connected = True

    @Cog.listener("on_disconnect")
    async def on_disconnect(self):
        if self.is_connected:
            await self.send_down_message()
        self.is_connected = False

    async def cog_load(self):
        if self.welcome_ch is None:
            self.welcome_ch = await self.bot.fetch_channel(WELCOME.id)
        await self.find_litmus_message()
        return await super().cog_load()

    @property
    async def message(self) -> Message:
        """Different from `find_litmus_message` bc this only finds it if its not set yet"""
        if self._message is None:
            await self.find_litmus_message()
        return self._message

    async def find_litmus_message(self) -> Message:
        old = self._message
        async for msg in self.welcome_ch.history(limit=5):
            if LitmusTest.is_litmus_message(msg):
                self._message = msg
                break
        if self._message is None and old is None: # no message found
            self._message = await self.welcome_ch.send(
                self.UP_MESSAGE,
                view=self.view
                )
        return self._message

    @property
    def view(self) -> View:
        return View().add_item(TakeLitmusButton())

    @staticmethod
    def is_litmus_message(msg: Message) -> bool:
        return msg.content.find("## Litmus Test") != -1


async def setup(bot: Bot):
    await bot.add_cog(LitmusTest(bot))
