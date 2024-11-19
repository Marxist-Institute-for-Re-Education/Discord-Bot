from datetime import timedelta

from discord import Poll, Interaction, Embed, Color, Guild
from discord.ui import Modal, TextInput
from discord.ext.commands import has_role

from utils import get, require_role
from utils.channels import DEM_DECISIONS, DEM_VOTE
from utils.roles import CADRE


class MotionPoll(Poll):
    def __init__(self):
        super().__init__(
            question = "Vote to pass or reject the measure:",
            timedelta = timedelta(days=1),
        )
        self.add_answer("Yea", emoji="✅")
        self.add_answer("Nay", emoji="❌")
        self.add_answer("Abstain")

    @property
    def yea(self) -> int:
        return self.answers[0].vote_count

    @property
    def nay(self) -> int:
        return self.answers[1].vote_count


class MotionModalBase(Modal, title = "Measure Details"):
    SYNOPSIS: TextInput = TextInput(label = "Synopsis", row = 0)
    DESCRIPTION: TextInput = TextInput(label = "Description", row = 1)

    def __init__(self, guild: Guild):
        super().__init__(timeout=None)
        self.guild = guild
        self.decisions_channel = guild.get_channel(DEM_DECISIONS.id)

    async def on_submit(self, interaction: Interaction):
        self.synop = self.SYNOPSIS.value
        self.desc = self.DESCRIPTION.value
        self.embed = Embed(
            title = self.synop,
            description = f"Description:\n{self.desc}\n\nProposed by {interaction.user}",
            color = Color.brand_green()
            )
        await interaction.response.defer()

    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_role(interaction.user)


class MotionModal(MotionModalBase):
    async def on_submit(self, interaction: Interaction):
        await super().on_submit(interaction)
        vote_channel = self.guild.get_channel(DEM_VOTE.id)
        poll = MotionPoll()
        msg = await vote_channel.send(embed=self.embed, poll=poll, silent=True)
        while not poll.is_finalized():
            continue
        if poll.yea > poll.nay:
            await self.decisions_channel.send(
                f"Motion passed by {poll.yea}/{poll.nay} majority vote",
                embed=self.embed,
                reference=msg
                )
        else:
            pass

class ExecDecisionModal(MotionModalBase):
    async def on_submit(self, interaction: Interaction):
        await super().on_submit(interaction)
        await self.decisions_channel.send(
            f"Motion passed by executive decision of {interaction.user.mention}",
            embed=self.embed,
            )


    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_role(interaction.user, CADRE, "Cadre")


__all__ = [
    "MotionModal",
    "ExecDecisionModal"
]
