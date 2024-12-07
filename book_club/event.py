import datetime as dt
from discord import Guild
from discord.scheduled_event import ScheduledEvent
from discord.utils import utcnow


class Meeting:
    @staticmethod
    def get_default_next() -> dt.datetime:
        DAY_OF_WEEK = 5 # Saturday
        HOUR = 15 # 3:00
        now = utcnow()
        diff = dt.timedelta((7 + DAY_OF_WEEK - now.weekday()) % 7)
        now = now + diff
        now.replace(hour=HOUR, minute=0, second=0, microsecond=0)
        pass

    def __init__(self, book: str, chapter_info: str):
        self.book: str = book
        self.chapter_info: str = chapter_info
        self.time: dt.datetime = self.default_next_time()

    async def create(self, guild: Guild) -> ScheduledEvent:
        return await guild.create_scheduled_event(
            name = "Book Club",
            description = self.format_description(),
            start_time = self.time
            )

    def format_description(self) -> str:
        desc = f"Book: *{self.book}*"
        if len(self.chapter_info) > 0:
            desc += "\nChapter(s): " + self.chapter_info
        return desc
