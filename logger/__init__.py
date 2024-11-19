import logging
from .color_formatter import ColorFormatter


logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(ColorFormatter())
file_handler = logging.FileHandler("discord.log")


logger.addHandler(handler)


def config():
    logging.basicConfig()

