import logging # avoids cirular import

import discord.ui as dc
from discord import PartialEmoji, Interaction
from discord.ui import Modal

from .typing import Type


__all__ = [
    "Button",
    "ModalButton"
]


class Button(dc.Button):
    EMOJI: PartialEmoji

    def __init_subclass__(cls, *, emoji: str):
        cls.EMOJI = PartialEmoji.from_str(emoji)

    def __init__(self):
        super().__init__(emoji=self.EMOJI)


class ModalButton(dc.Button):
    EMOJI: PartialEmoji
    MODAL_CLASS: Type[Modal]

    def __init_subclass__(cls, *, emoji: str, modal: Type[Modal]):
        cls.EMOJI = PartialEmoji.from_str(emoji)
        cls.MODAL_CLASS = modal

    def __init__(self):
        super().__init__(emoji=self.EMOJI)

    async def callback(self, interaction: Interaction):
        logger = logging.getLogger("main") # used instead of `logger.get_main_logger` bc of circular import
        logger.debug(f"user {interaction.user} used button ({self.MODAL_CLASS.__name__})")
        await interaction.response.send_modal(self.MODAL_CLASS())
