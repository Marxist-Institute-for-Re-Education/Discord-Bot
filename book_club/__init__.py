from discord.ui import View
from discord.ext.commands import Context, Cog, command, Bot

from utils import get, is_lit_chair
from .elements import *


class BookClub(Cog, name = "Book Club"):
    """Everything related to Book Club!"""

    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @command(help="View the current Book Club book suggestion list")
    async def suggestions(self, ctx: Context):
        embed = suggestions_embed()
        view = View()
        view.add_item(AddButton())
        view.add_item(RemoveButton())
        view.add_item(EditButton())
        if not is_lit_chair(ctx.author):
            view.add_item(PrioritizeButton())
        return await ctx.send(embed=embed, view=view)

    # @command(help="Set the next work to be read for Book Club")
    # async def assign(self, ctx: Context):
    #     await ctx.send(
    #         "What work are you selecting?",
    #         view=View().add_item(AssignDropdown())
    #         )

    # @Cog.listener(name="on_scheduled_event_update")
    # async def book_club_meeting(self, before: ScheduledEvent, after: ScheduledEvent):
    #     if after.name != "Book Club":
    #         return
    #     if before.status == after.status:
    #         return
    #     if before.status == EventStatus.active and after.status == EventStatus.completed:
    #         category = get(after.guild.categories, name="Book Club")
    #         # event has completed
    #         vc = after.channel or category.voice_channels[0]
    #         # wait for everyone to leave VC
    #         if isinstance(vc, VoiceChannel):
    #             while len(vc.members) > 0:
    #                 continue
    #         lit_chair = os.getenv("ROSE_ID")
    #         nexts = Suggestion.get_next()
    #         if len(nexts) == 1:
    #             announcements: TextChannel = get(category.text_channels, name="announcements")
    #             # next work is automatically determined
    #             # TODO: have the bot do a whole lot more
    #             nexts[0].activate()
    #             return await announcements.send(
    #                 "Good work comrades!\n"
    #                 "# Next Work :bangbang:\n"
    #                 f"The next work will be **{nexts[0].title}**!\n\n"
    #                 f"{lit_chair.mention} will provide links shortly."
    #             )
    #         else:
    #             polls: TextChannel = get(category.text_channels, name="polls")
    #             poll = Poll(
    #                 question="What should we study next?",
    #                 duration=timedelta(days=1.0)
    #                 )
    #             for entry in nexts:
    #                 poll.add_answer(text=entry.title)
    #             return await polls.send("Great study session comrades!", poll=poll)

    async def cog_check(self, ctx: Context) -> bool:
        return get(ctx.author.roles, name="Book Club") is not None

async def setup(bot: Bot):
    await bot.add_cog(BookClub(bot))

__all__ = [
    "BookClub",
    "setup"
]
