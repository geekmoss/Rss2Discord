import sys

from Rss2Discord import (
    load, load_simple, Memory, make_embed, revert_feeds_to_hooks, Timer
)
from Rss2Discord.models import (
    Post, Hook, RssFeed, RssFeedMode, load_feeds, load_hooks
)
from time import sleep
import requests
import click
import os


@click.command()
@click.option('--interval', type=click.INT, help='Interval between crawl; env INTERVAL or 60',
              default=os.environ.get('INTERVAL', 60))
@click.option('--only-build-memory', is_flag=True)
@click.option('--verbose', '-v', is_flag=True)
def cli(interval: int, only_build_memory: bool = False, verbose: bool = False):
    def v(*args, **kwargs):
        if verbose:
            click.echo(*args, err=True, **kwargs)
            sys.stdout.flush()
            pass
        pass

    mem = Memory('memory.msgpack')
    timer = Timer()

    feeds = load_feeds('config.yaml')
    hooks = load_hooks('config.yaml')
    feeds_to_hooks = revert_feeds_to_hooks(hooks)

    while True:
        v('Running...')
        for feed_name, feed in feeds.items():
            if (feed.interval or interval) > timer.get_interval(feed_name):
                v(f'Too soon for {feed_name}...')
                continue

            # Just sent list of links
            if feed.simple_link:
                urls = [u for u in load_simple(feed.url) if not mem.is_new(feed_name, u)]
                if len(urls) == 0:
                    timer.set_tick(feed_name)
                    continue

                v(f'For {feed_name} found new {len(urls)} urls')
                mem.save_ids(feed_name, set(urls))

                # If only build memory - skip posting
                if only_build_memory:
                    continue

                for hook in feeds_to_hooks.get(feed_name, []):
                    v(f'Sending {feed_name} to {hook}')
                    res = requests.post(hook, json={'content': '\n'.join(urls)})
                    v(f'{res.status_code}')
                    if 200 > res.status_code or res.status_code >= 300:
                        print(f'Feed {feed_name}, hook {hook} returns {res.status_code}')
                    pass
            # Post embeds
            else:
                new_posts = [p for p in load(feed.url) if not mem.is_new(feed_name, f'{p.id}')]
                if len(new_posts) == 0:
                    timer.set_tick(feed_name)
                    continue

                mem.save_ids(feed_name, set([p.id for p in new_posts]))

                v(f'For {feed_name} found new {len(new_posts)} posts')

                for i in range((len(new_posts) // 10) + (1 if len(new_posts) % 10 > 0 else 0)):
                    embeds = []
                    for r in new_posts[i * 10:(i + 1) * 10]:
                        embeds.append(make_embed(r))
                        pass

                    # If only build memory - skip posting
                    if only_build_memory:
                        continue

                    for hook in feeds_to_hooks.get(feed_name, []):
                        v(f'Sending {feed_name} to {hook}')

                        res = requests.post(
                            url=hook,
                            json={
                                'content': None,
                                'embeds': embeds,
                            }
                        )
                        v(f'{res.status_code}')

                        if 200 > res.status_code or res.status_code >= 300:
                            print(f'Feed {feed_name}, hook {hook} returns {res.status_code}')
                        pass
                    pass
                pass

            timer.set_tick(feed_name)
            pass

        # Only build and leave
        if only_build_memory:
            break

        sleep(5)
    pass


if __name__ == '__main__':
    print('Starting')
    sys.stdout.flush()
    cli()
    pass
