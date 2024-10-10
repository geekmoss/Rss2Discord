from Rss2Discord.Core import Memory, Timer
from Rss2Discord.parse import load, load_simple
from Rss2Discord.Utils import revert_feeds_to_hooks, logger
from Rss2Discord.Discord import make_embed
from Rss2Discord.Models import (
    RssFeed, load_feeds, load_hooks
)
import requests


class CML:
    def __init__(self, interval: int, verbose: bool, config_file: str = 'config.yaml',
                 memory_file: str = 'memory.msgpack'):
        if verbose:
            logger.setLevel('DEBUG' if verbose else 'INFO')

        self.__interval = interval

        self.mem = Memory(memory_file)
        self.timer = Timer()

        self.feeds = load_feeds(config_file)
        self.hooks = load_hooks(config_file)
        self.feeds_to_hooks = revert_feeds_to_hooks(self.hooks)

    def build_mem_only(self):
        for feed_name, feed in self.feeds.items():
            if feed.simple_link:
                self._crawl_simple_feed(feed_name, feed)
            else:
                self._crawl_embed_feed(feed_name, feed)

    def do_crawl_and_post(self):
        logger.debug("Starting check and crawl loop")

        for feed_name, feed in self.feeds.items():
            if (feed.interval or self.__interval) > self.timer.get_interval(feed_name):
                logger.debug(f'Too soon for {feed_name}...')
                continue

            if feed.simple_link:
                urls = self._crawl_simple_feed(feed_name, feed)
                if len(urls) == 0:
                    continue

                for hook in self.feeds_to_hooks.get(feed_name, []):
                    logger.debug(f'Sending {feed_name} to {hook} with {len(urls)} urls')
                    res = requests.post(hook, json={'content': '\n'.join(urls)})
                    if 200 > res.status_code or res.status_code >= 300:
                        logger.error(f'Feed {feed_name}, hook {hook} returns {res.status_code}')
                        logger.error(res.text)
                    pass
                pass
            else:
                new_posts = self._crawl_embed_feed(feed_name, feed)

                for i in range((len(new_posts) // 10) + (1 if len(new_posts) % 10 > 0 else 0)):
                    embeds = []
                    for r in new_posts[i * 10:(i + 1) * 10]:
                        embeds.append(make_embed(r))
                        pass

                    for hook in self.feeds_to_hooks.get(feed_name, []):
                        logger.debug(f'Sending {feed_name} to {hook}')
                        res = requests.post(
                            url=hook,
                            json={
                                'content': None,
                                'embeds': embeds,
                            }
                        )
                        if 200 > res.status_code or res.status_code >= 300:
                            logger.error(f'Feed {feed_name}, hook {hook} returns {res.status_code}')
                            pass
                        pass
                    pass
                pass
            pass
        pass

    def _crawl_simple_feed(self, feed_name: str, feed: RssFeed) -> list[str]:
        urls = [u for u in load_simple(feed.url) if not self.mem.is_new(feed_name, u)]
        if len(urls) == 0:
            self.timer.set_tick(feed_name)
            return []

        logger.info(f'For {feed_name} found new {len(urls)} urls.')
        self.mem.save_ids(feed_name, set(urls))
        return urls

    def _crawl_embed_feed(self, feed_name: str, feed: RssFeed):
        new_posts = [p for p in load(feed.url) if not self.mem.is_new(feed_name, f'{p.id}')]
        if len(new_posts) == 0:
            self.timer.set_tick(feed_name)
            return []

        logger.info(f'For {feed_name} found new {len(new_posts)} posts.')
        self.mem.save_ids(feed_name, set([p.id for p in new_posts]))
        return new_posts
