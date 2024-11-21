import logging
from logging import LogRecord, Formatter
from .style import Style


__all__ = [
    "BasicFormatter",
    "ColorFormatter",
]


class BasicFormatter(Formatter):
    TIME_FORMAT = "Y%Y/M%m/D%d-%H:%M:%S"
    FORMAT = "~~~ {levelname}:{name}:{funcName}: [{asctime}]\n\t{message}"

    def __init__(self):
        super().__init__(fmt=self.FORMAT, datefmt=self.TIME_FORMAT, style='{')


class ColorFormatter(BasicFormatter):
    FORMAT = "~~~ {levelname}:" + Style.DIM(
        "{module}:{funcName}:" + Style.BLUE(" [{asctime}]")
        ) + "\n\t{message}"
    FORMATS = {
        logging.DEBUG: Style.PURPLE,
        logging.INFO: Style.BLUE,
        logging.WARNING: Style.YELLOW,
        logging.ERROR: Style.RED,
        logging.CRITICAL: Style.RED + Style.BOLD,
        }

    def format(self, record):
        fmt = self.FORMAT
        fmt = self.format_level(fmt, record)
        fmtr = Formatter(fmt=fmt, datefmt=self.TIME_FORMAT, style='{')
        return fmtr.format(record)

    def format_level(self, fmt: str, record: LogRecord) -> str:
        style = self.FORMATS.get(record.levelno) + Style.UNDERLINE
        return style.substr(fmt, "{levelname}")

### TESTS


