from datetime import timedelta

from discord import Poll, Member, Interaction, Guild
from discord.ui import Select, View
from discord.ext.commands import Cog, Bot, command, Context, has_role

from utils import get, require_role
from utils.roles import CADRE, CENTRAL_COMMITTEE
from .measure import *


__all__ = [
    "Democracy"
]


class Democracy(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        super().__init__()

    @command(help="Motion to pass a measure")
    async def motion(self, ctx: Context):
        view = View().add_item(MotionModal(ctx.guild))
        await ctx.send(view=view)

    @command(name="exec", help="Pass a measure by executive decision")
    @has_role(CENTRAL_COMMITTEE)
    async def exec_decision(self, ctx: Context):
        view = View().add_item(ExecDecisionModal(ctx.guild))
        await ctx.send(view=view)

    @command(help="Nominate someone for a position", hidden=True)
    async def nominate(self, ctx: Context, user: Member = None):
        pass

    async def cog_check(self, ctx: Context) -> bool:
        return require_role(ctx.author, CADRE, "Cadre")

    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_role(interaction.author, CADRE, "Cadre")


# class Election:
#     def __init__(self, guild: Guild, position: str):
#         self.position: str = position
#         self.users: list[Member] = []

#     def add_user(self, user: Member):
#         self.users.append(user)

#     def poll(self) -> Poll:
#         poll = Poll(
#             question=f"Who would you like to vote for the position of {self.position}",
#             duration=timedelta(days=1.0)
#         )
#         pass

# class ElectionDropdown(Select):
#     def __init__(self, guild: Guild, nom: Election):
#         super().__init__()
#         self.guild = guild
#         self.cadre = get(guild.roles, name="Cadre")
#         self.nom = nom
#         for user in self.cadre.members:
#             self.add_option(label=user.name, value=user.id)

#     async def callback(self, interaction: Interaction):
#         user = self.guild.get_member(self.values[0])
#         self.nom.add_user(user)


async def setup(bot: Bot):
    await bot.add_cog(Democracy(bot))
