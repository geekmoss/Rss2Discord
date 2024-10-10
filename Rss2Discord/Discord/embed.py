from datetime import timezone
from Rss2Discord.Models import Post


def make_embed(p: Post):
    content = f'{p.summary}'

    img = p.thumbnail

    return {
        'url': p.link,
        'thumbnail': {
            'url': img,
        },
        'color': 0xefd613,
        'timestamp':
            p.published.astimezone(timezone.utc).isoformat(timespec='milliseconds'),
        'title': p.title,
        'description': content,
        'footer': {
            'text': p.author,
        },
    }