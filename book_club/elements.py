from discord import Member, Interaction, TextStyle, Embed
from discord.ext.commands.errors import CheckFailure
from discord.ui import Modal, View, TextInput, Select
from typing import List

from utils import is_lit_chair, abbreviate, Button, ModalButton
from utils.roles import CADRE
from database import Suggestion, new_session


__all__ = [
    "AddButton",
    "EditButton",
    "RemoveButton",
    "PrioritizeButton",
    "suggestions_embed"
]


def suggestions_embed() -> Embed:
    titles = []
    for sug in sorted(Suggestion.all(), key=lambda s: s.status):
        titles.append(sug.display_title())
    return Embed(
        title="Suggested works:",
        description="\n".join(titles)
        )


class SuggestionsDropdown(Select):
    def __init__(self):
        super().__init__()
        for entry in Suggestion.all():
            self.add_option(label=abbreviate(entry.title), value=entry.title)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer()
        await interaction.message.edit(embed=suggestions_embed())

    def get_all(self) -> List[Suggestion]:
        return [Suggestion.get(title) for title in self.values]

    def get(self) -> Suggestion:
        return Suggestion.get(self.values[0])

class UserSuggestionsDropdown(SuggestionsDropdown):
    def __init__(self, user: Member):
        super(SuggestionsDropdown, self).__init__()
        for entry in Suggestion.from_user(user.id):
            self.add_option(label=abbreviate(entry.title), value=entry.title)


class AddModal(Modal, title="Add"):
    TITLE: TextInput = TextInput(
        label = "Title",
        required = True,
        row = 0
        )
    CHAPTERS: TextInput = TextInput(
        label = "Number of chapters/sections",
        required = False,
        placeholder = "(leave blank if there are none)",
        row = 1
        )
    NOTES: TextInput = TextInput(
        label = "Notes",
        style = TextStyle.long,
        required = True,
        row = 2
        )

    async def on_submit(self, interaction: Interaction):
        user = interaction.user
        title = self.TITLE.value
        chapters: str = self.CHAPTERS.value
        total_ch = 0
        if chapters is not None and len(chapters) > 0:
            total_ch = int(chapters)
        notes = self.NOTES.value
        Suggestion.new(title, user.id, total_ch, notes)
        await interaction.response.defer()
        await interaction.message.edit(embed=suggestions_embed())

class AddButton(ModalButton, emoji="➕", modal=AddModal):
    pass


class EditModal(Modal, title="Edit"):
    TITLE: TextInput = TextInput(
        label = "Title",
        required = True,
        row = 0
        )
    NEXT_CH: TextInput = TextInput(
        label = "Last-Read Chapter",
        required = False,
        placeholder = "0",
        row = 1
        )
    TOTAL_CH: TextInput = TextInput(
        label = "Total number of chapters/sections",
        required = False,
        placeholder = "(0 if none)",
        row = 2
        )
    NOTES: TextInput = TextInput(
        label = "Notes",
        style = TextStyle.long,
        required = True,
        row = 2
        )

    def __init__(self, title: str):
        super().__init__()
        self.suggestion = Suggestion.get(title)
        self.TITLE.default = self.suggestion.title
        self.NEXT_CH.default = self.suggestion.next_ch
        self.TOTAL_CH.default = self.suggestion.total_ch
        self.NOTES.default = self.suggestion.notes

    async def on_submit(self, interaction: Interaction):
        with new_session() as session:
            self.suggestion.title = self.TITLE.value
            next_ch = self.NEXT_CH.value
            if len(next_ch) > 0:
                self.suggestion.next_ch = int(next_ch)
            total_ch = self.TOTAL_CH.value
            if len(total_ch) > 0:
                self.suggestion.total_ch = int(total_ch)
            self.notes = self.NOTES.value
            session.commit()
        await interaction.response.defer()
        await interaction.message.edit(embed=suggestions_embed())

class EditDropdown(UserSuggestionsDropdown):
    async def callback(self, interaction: Interaction):
        doc_id = int(self.values[0])
        await interaction.response.send_modal(EditModal(doc_id))

class EditButton(Button, emoji="📝"):
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(
            "Which suggestions would you like to edit?",
            view=View().add_item(EditDropdown(interaction.user)),
            ephemeral=True
            )


class RemoveDropdown(UserSuggestionsDropdown):
    async def callback(self, interaction: Interaction):
        for entry in self.values:
            entry.remove()
        await super().callback(interaction)

class RemoveButton(Button, emoji="❌"):
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(
            "Which suggestions would you like to remove?",
            view=View().add_item(RemoveDropdown(interaction.user)),
            ephemeral=True
            )


class AssignDropdown(SuggestionsDropdown):
    def __init__(self):
        for entry in Suggestion.all():
            self.add_option(
                label = entry.title,
                value = entry.doc_id,
                default = entry.is_prioritized
            )

    async def callback(self, interaction: Interaction):
        for entry in self.get_all():
            entry.activate()
        await super().callback(interaction)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if not is_lit_chair(interaction.user):
            raise CheckFailure(f"{interaction.user} is not a Literature Chair")
        return True


class PrioritizeDropdown(SuggestionsDropdown):
    def __init__(self):
        all = Suggestion.all()
        super(SuggestionsDropdown, self).__init__(min_values=0, max_values=len(all))
        for entry in all:
            self.add_option(
                label = entry.title,
                value = entry.doc_id,
                default = entry.is_prioritized
            )

    async def callback(self, interaction: Interaction):
        for sug in self.get_all():
            sug.is_prioritized = True
        await super().callback(interaction)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if not is_lit_chair(interaction.user):
            raise CheckFailure(f"{interaction.user} is not a Literature Chair")
        return True

class PrioritizeButton(Button, emoji="❗"):
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(
            "What would you like to prioritize?",
            view=View().add_item(PrioritizeDropdown()),
            ephemeral=True
            )

    async def interaction_check(self, interaction: Interaction) -> bool:
        if not is_lit_chair(interaction.user):
            raise CheckFailure(f"{interaction.user} is not a Literature Chair")
        return True

