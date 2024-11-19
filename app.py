import os
from bot import *
from dotenv import load_dotenv

import book_club
import committee
import democracy
import litmus


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
