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

    async def cog_load(self):
        channel: TextChannel = await self.bot.fetch_channel(WELCOME.id)
        last_msg = channel.last_message
        last_msg = last_msg or await anext(channel.history(limit=1))
        if last_msg.author != self.bot.user:
            # print(f"DEBUG: author: {last_msg.author} | {self.bot}")
            await channel.send(
                "## Litmus Test\n"
                "Interact with the button below to submit your litmus test!",
                view=self.view
            )
        else:
            await last_msg.edit(view=self.view)

    @property
    def view(self) -> View:
        return View().add_item(TakeLitmusButton())


async def setup(bot: Bot):
    await bot.add_cog(LitmusTest(bot))
