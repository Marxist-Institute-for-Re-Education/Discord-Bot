import logging
from logging import StreamHandler, FileHandler, getLogger

from .formatters import ColorFormatter, BasicFormatter


__all__ = [
    "config_loggers",
    "getLogger",
]


def create_file_handler(fname: str, level) -> FileHandler:
    hdlr = FileHandler(fname, mode="w", encoding="utf-8")
    hdlr.setFormatter(BasicFormatter())
    hdlr.setLevel(level)
    return hdlr


def config_loggers():
    stream_handler = StreamHandler()
    stream_handler.setFormatter(ColorFormatter())
    stream_handler.setLevel(logging.INFO)

    debug_hdlr = create_file_handler("logs/debug.log", logging.DEBUG)
    dc_debug_hdlr = create_file_handler("logs/discord-debug.log", logging.DEBUG)

    dc_logger = logging.getLogger("discord")
    dc_logger.setLevel(logging.DEBUG)
    dc_logger.addHandler(stream_handler)
    dc_logger.addHandler(dc_debug_hdlr)
    dc_logger.propagate = False

    root = getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(stream_handler)
    root.addHandler(debug_hdlr)
