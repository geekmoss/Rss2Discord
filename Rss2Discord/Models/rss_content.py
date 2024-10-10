from dataclasses import dataclass
from datetime import timedelta, datetime
from enum import Enum


class SyUpdate:
    class UpdatePeriod(Enum):
        HOURLY = 'hourly'
        DAILY = 'daily'
        WEEKLY = 'weekly'
        MONTHLY = 'monthly'
        YEARLY = 'yearly'
        pass

    period: UpdatePeriod
    frequency: int

    def __init__(self, period, frequency: int):
        self.period = self.UpdatePeriod(period)
        self.frequency = int(frequency)

    def get_timedelta(self) -> timedelta:
        match self.period:
            case self.UpdatePeriod.HOURLY:
                return timedelta(hours=self.frequency)
            case self.UpdatePeriod.DAILY:
                return timedelta(days=self.frequency)
            case self.UpdatePeriod.WEEKLY:
                return timedelta(days=self.frequency * 7)
            case self.UpdatePeriod.MONTHLY:
                return timedelta(days=self.frequency * 30)
            case self.UpdatePeriod.YEARLY:
                return timedelta(days=self.frequency * 365)


@dataclass
class Tag:
    term: str
    scheme: str = None
    label: str = None


@dataclass
class Post:
    id: str
    title: str
    link: str
    author: str | None
    authors: [str]
    published: datetime | None
    tags: [Tag]
    summary: str
    thumbnail: str | None
