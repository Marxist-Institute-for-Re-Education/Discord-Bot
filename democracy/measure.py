from datetime import timedelta

from discord import Poll, Interaction, Embed, Color, Guild
from discord.ui import Modal, TextInput
from discord.ext.commands import has_role

from utils.roles import require_role
from utils.channels import DEM_DECISIONS, DEM_VOTE
from utils.roles import CADRE
from logger import getLogger


__all__ = [
    "MotionModal",
    "ExecDecisionModal"
]


logger = getLogger(__name__)


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
        user = interaction.user
        self.synop = self.SYNOPSIS.value
        logger.info(f"user {user} proposed to motion\n\t\tsynopsis: {self.synop}")
        self.desc = self.DESCRIPTION.value
        self.embed = Embed(
            title = self.synop,
            description = f"Description:\n{self.desc}",
            color = Color.brand_green()
            ).set_footer(text=f"Proposed by {user}")
        logger.debug(
            f"motion by {user}:"
            f"\n\t\tsynopsis: {self.synop}\n\t\tdescription: {self.desc}"
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
        logger.debug(f"sent poll for motion (ID:{msg.id})")
        while not poll.is_finalized():
            continue
        logger.info(f"poll for motion (ID:{msg.id}) finished.")
        if poll.yea > poll.nay:
            await self.decisions_channel.send(
                f"Motion passed by {poll.yea}/{poll.nay} majority vote",
                embed=self.embed,
                reference=msg
                )
        else:
            await self.decisions_channel.send(
                f"Motion passed by {poll.yea}/{poll.nay} majority vote",
                embed=self.embed,
                reference=msg
                )
            logger.info(f"motion failed to pass (yea: {poll.yea}; nay: {poll.nay})")

class ExecDecisionModal(MotionModalBase):
    async def on_submit(self, interaction: Interaction):
        user = interaction.user
        logger.info(f"user {user} passed motion by executive decision")
        await super().on_submit(interaction)
        await self.decisions_channel.send(
            f"Motion passed by executive decision of {user.mention}",
            embed=self.embed,
            )

    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_role(interaction.user, CADRE, "Cadre")
