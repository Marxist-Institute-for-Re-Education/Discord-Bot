import logging
from logging import LogRecord, Formatter
from .style import Style


FORMAT = "~~~ {levelname}:{module}:{funcName}: [{asctime}] \n\t{message}"

class ColorFormatter(Formatter):

    TIME_FORMAT = "Y%Y/M%m/D%d-%H:%M:%S"
    FORMATS = {
        logging.DEBUG: Style.MAGENTA,
        logging.INFO: Style.BLUE,
        logging.WARNING: Style.YELLOW,
        logging.ERROR: Style.RED,
        logging.CRITICAL: Style.RED,
        }

    def __init__(self):
        super().__init__(fmt=self.FORMAT, datefmt=self.TIME_FORMAT, style='{')

    def format(self, record):
        fmt = self.FORMAT
        fmt = self.format_level(fmt, record)
        fmt = Style.DIM.substr(fmt, ":{module}:{funcName}:")
        fmtr = Formatter(fmt=fmt, datefmt=self.TIME_FORMAT, style='{')
        return fmtr.format(record)

    def format_level(self, fmt: str, record: LogRecord) -> str:
        style = self.FORMATS.get(record.levelno) + Style.UNDERLINE
        return style.substr(fmt, "{levelname}")