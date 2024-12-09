import os
from bot import MireBot
from dotenv import load_dotenv

import book_club
import committee
import democracy
import litmus
import logger


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def main():
    # `log_handler`` is `None` bc we do our own setup with `config()`
    bot = MireBot()
    logger.config_loggers()
    bot.run(TOKEN, log_handler=None)

if __name__ == "__main__":
    main()
