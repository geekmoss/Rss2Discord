from pydantic import BaseModel, Field
from enum import Enum
import yaml


class RssFeedMode(str, Enum):
    feed = 'feed'
    diff = 'diff'


class RssFeed(BaseModel):
    url: str
    mode: RssFeedMode = RssFeedMode.feed
    color: int = 0xefd613
    simple_link: bool = False
    interval: int | None = Field(ge=10, description='Crawl interval in minutes, None for global interval', default=None)
    drop_html: bool = False
    unwrap_html: bool = False


def parse_yaml(file: str) -> dict[str, RssFeed]:
    with open(file) as f:
        root: dict = yaml.safe_load(f)

    feeds = {}
    for feed, data in (root.get('rss') or {}).items():
        feeds[feed] = RssFeed(url=data) if isinstance(data, str) else RssFeed.model_validate(data)

    return feeds
