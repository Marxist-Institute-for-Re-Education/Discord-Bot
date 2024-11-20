import logging
from .color_formatter import ColorFormatter, BasicFormatter


def config():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(ColorFormatter())
    stream_handler.setLevel(logging.INFO)
    file_handler = logging.FileHandler("discord.log")
    file_handler.setFormatter(BasicFormatter())
    file_handler.setLevel(logging.DEBUG)

    dc_logger = logging.getLogger("discord")
    dc_logger.setLevel(logging.DEBUG)
    dc_logger.addHandler(stream_handler)
    dc_logger.addHandler(file_handler)
    main_logger = logging.getLogger("main")
    main_logger.setLevel(logging.INFO)
    main_logger.addHandler(stream_handler)

    main_logger.addHandler(stream_handler)
    main_logger.addHandler(file_handler)

