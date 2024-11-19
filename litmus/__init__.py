from discord import Message, TextChannel, PartialMessage
from discord.ui import View, Button
from discord.ext.commands import Context, Cog, command, Bot

from utils.channels import WELCOME
from .elements import TakeLitmusButton


class LitmusTest(Cog, name = "Litmus Test"):
    UP_MESSAGE = "## Litmus Test\nInteract with the button below to submit your litmus test!"
    DOWN_MESSAGE = "## Litmus Test\nBot is currently down, please reach out to a CC member!"

    def __init__(self, bot: Bot):
        super().__init__()
        self.bot: Bot = bot
        self.welcome_ch = bot.get_channel(WELCOME.id)
        self.message: Message = None

    async def cog_load(self):
        if self.welcome_ch is None:
            self.welcome_ch = await self.bot.fetch_channel(WELCOME.id)
        await self.find_litmus_message()
        await self.message.edit(content=self.UP_MESSAGE, view=self.view)
        return await super().cog_load()

    async def cog_unload(self):
        await self.message.edit(self.DOWN_MESSAGE, view=None)
        return await super().cog_unload()

    async def find_litmus_message(self) -> Message:
        if self.message is None:
            async for msg in self.welcome_ch.history(limit=5):
                if LitmusTest.is_litmus_message(msg):
                    self.message = msg
                    break
        if self.message is None: # if there was no message found
            self.message = await self.welcome_ch.send(
                self.UP_MESSAGE,
                view=self.view
                )
        return self.message

    @property
    def view(self) -> View:
        return View().add_item(TakeLitmusButton())

    @staticmethod
    def is_litmus_message(msg: Message) -> bool:
        return msg.content.find("## Litmus Test") != -1


async def setup(bot: Bot):
    await bot.add_cog(LitmusTest(bot))
