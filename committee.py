from discord import Member, Role
from discord.utils import get
from discord.ext.commands.errors import MissingRequiredArgument, BadArgument
from discord.ext.commands import Context, Cog, command, Bot


class Committee(Cog, name = "Committee"):
    """Everything related to Book Club!"""
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @command(name="join", help="Join a committee!")
    async def join_committee(self, ctx: Context, committee_role: Role=None, user: Member=None):
        print(f"Adding @{user} to @{committee_role}")
        if user is None:
            user = ctx.author
        if committee_role is None:
            await ctx.send("Please specify what committee you'd like to join")
            raise MissingRequiredArgument("committee")
        if not committee_role.name.endswith(" Committee"):
            await ctx.send(f"{committee_role} is not a valid committee role. Please try again.")
            raise BadArgument("committee")
        return await user.add_roles(committee_role)

    # notifies a committee's channel when someone has joined
    @Cog.listener("on_member_update")
    async def notify_committee(self, before: Member, after: Member):
        if len(before.roles) < len(after.roles):
            role = next(role for role in after.roles if role not in before.roles)
            if role.name.endswith(" Committee"):
                channel_name = role.name.lower().replace(' ', '-')
                channel = get(role.guild.text_channels, name=channel_name)
                await channel.send(f"{after.mention} has joined the {role.name}!!")

    # possible command: task creation

async def setup(bot: Bot):
    await bot.add_cog(Committee(bot))

__all__ = [
    "Committee",
    "setup"
]
