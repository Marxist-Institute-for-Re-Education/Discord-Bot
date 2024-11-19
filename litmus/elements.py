from discord import Interaction, Embed, Member, TextStyle, ChannelType, PartialEmoji
from discord.threads import Thread
from discord.colour import Color
from discord.channel import TextChannel
from discord.ui import Button, Modal, View
from discord.ui.text_input import TextInput

from utils import ModalButton, require_non_member, require_role
from utils.channels import LITMUS_TESTS, WELCOME
from utils.roles import GENERAL_MEMBER, CENTRAL_COMMITTEE


class LitmusTestModal(Modal):
    TENDENCY: TextInput = TextInput(
        label = "What is your tendency?",
        placeholder = "Marxist-Leninist, Anarchist, MLM-G, etc...",
        row = 0
        )
    PALI_SOLUTION: TextInput = TextInput(
        label = "What solution do you support for palestine?",
        placeholder = "Two-state, one palestinian state, 1948, etc...",
        row = 1
        )
    ORGS: TextInput = TextInput(
        label = "What other orgs are you a part of?",
        placeholder = "SJP, PSL, CPUSA, ACP, DSA, SDS, FRSO, etc...",
        row = 2
        )
    WHY: TextInput = TextInput(
        label = "Why would you like to join?",
        style = TextStyle.long,
        row = 3
    )
    HOW: TextInput = TextInput(
        label = "Do you have any interest in becoming a Cadre?",
        placeholder = "Instagram, TikTok, invited by @user, etc...",
        required = False,
        row = 3
        )

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        output = interaction.guild.get_channel(LITMUS_TESTS.id)
        user = interaction.user
        embed = Embed(
            title = f"{user}'s Litmus Test",
            description = self.fmt_inputs()
            )
        view = View()
        view.add_item(ApproveButton(user))
        view.add_item(FollowUpButton(user))
        view.add_item(DenyButton(user))
        await output.send(embed=embed, view=view)

    def fmt_inputs(self) -> str:
        inputs = [self.TENDENCY, self.PALI_SOLUTION, self.ORGS, self.WHY]
        desc: str = ""
        for i, input in enumerate(inputs):
            desc += f"{i}) **{input.label}**\n{input.value}\n\n"
        return desc.rstrip()

    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_non_member(interaction.user)


class TakeLitmusButton(ModalButton, emoji="📝", modal=LitmusTestModal):
    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_non_member(interaction.user)


class CCButton(Button):
    EMOJI: PartialEmoji

    def __init_subclass__(cls, emoji: str):
        cls.EMOJI = emoji

    def __init__(self, user: Member):
        super().__init__(emoji=self.EMOJI)
        self.user = user

    async def interaction_check(self, interaction: Interaction) -> bool:
        return require_role(interaction.user, CENTRAL_COMMITTEE, "Central Committee")


class ApproveButton(CCButton, emoji="✅"):
    async def callback(self, interaction: Interaction):
        embed = interaction.message.embeds[0]
        embed.color = Color.brand_green()
        embed.set_footer(f"approved by {interaction.user.mention}")
        await interaction.response.edit_message(view=None, embed=embed)
        await self.user.add_roles(GENERAL_MEMBER)


class FollowUpButton(CCButton, emoji="💬"):
    async def callback(self, interaction: Interaction):
        embed = interaction.message.embeds[0]
        user = interaction.guild.get_member(self.user)
        embed.color = Color.dark_red() if user is None else Color.yellow()
        embed.set_footer(f"being followed up by {interaction.user.mention}")
        await interaction.response.edit_message(view=None, embed=embed)
        # create private thread
        welcome_channel: TextChannel = interaction.guild.get_channel(WELCOME.id)
        thread: Thread = await welcome_channel.create_thread(
            type = ChannelType.private_thread,
            name = f"Follow Up with {user.name}",
            invitable = False,
            )
        await thread.add_user(user)
        await thread.add_user(interaction.user)
        await thread.send(
            f"{user.mention} {interaction.user.mention}",
            embed=embed
            )


class DenyButton(CCButton, emoji="❌"):
    async def callback(self, interaction: Interaction):
        await interaction.response.send_modal(DenyModal(self.user))
        embed = interaction.message.embeds[0]
        embed.set_footer(f"Denied by {interaction.user.mention}")
        await interaction.followup.edit_message(embed=embed)
        # dm user
        pass

class DenyModal(Modal, title = "Denial"):
    REASON: TextInput = TextInput(
        label = "Reason for denial",
        min_length = 5
        )

    def __init__(self, user: Member):
        super().__init__()
        self.user = user

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer()
        dm = self.user.dm_channel
        if dm is None:
            dm = await self.user.create_dm()
        await dm.send(
            "Sorry, but MIRE has decided to deny your application.",
            embed = Embed(title="Reason:", description=self.REASON.value)
            )
