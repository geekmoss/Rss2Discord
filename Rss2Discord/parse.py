from datetime import timedelta, datetime
from time import mktime
from Rss2Discord.Models.rss_content import (
    Post,
    Tag,
)
import feedparser


def load_simple(url: str) -> list[str]:
    parser = feedparser.parse(url)
    urls = []

    for e in parser.entries:
        urls.append(e.link)

    return urls


def load(url: str) -> list[Post]:
    parser = feedparser.parse(url)

    posts = []
    for e in parser.entries:
        thumbnail = None
        for enclosure in e.enclosures:
            if enclosure['type'].startswith('image/'):
                thumbnail = enclosure['href']
                break

        posts.append(Post(
            id=e.id,
            title=e.title,
            link=e.link,
            author=e.author if hasattr(e, 'author') else '',
            authors=[a['name'] for a in e.authors] if hasattr(e, 'author') else '',
            published=datetime.fromtimestamp(mktime(e.published_parsed)) + timedelta(hours=1) if hasattr(e, 'published_parsed') else None,
            tags=[Tag(term=t['term'], scheme=t['scheme'], label=t['label']) for t in e.tags] if hasattr(e, 'tags') else [],
            summary=e.summary if hasattr(e, 'summary') else None,
            thumbnail=thumbnail,
        ))

    posts.sort(key=lambda x: x.published, reverse=True)
    return posts
