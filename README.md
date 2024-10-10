# Rss2Discord

Statically configured job that regularly crawls specified RSS feeds and sends them to specified Discord webhooks.

## Configuration Example:
```yaml
# Feed Configuration
rss:
  feed_just_link: https://blog1.website.net/rss
  my_blog:
    url: https://blog.my-site.org/feed
    color: 0xefd613  # Hex value of embeds for this feed, default is this value
    simple_link: no  # If set to yes, then only links are sent (Discord will load the embed from the link), so they are plain text messages.
    interval: null   # Override crawl check interval, in minutes, minimum is 10 minutes
# Hooks Configuration
webhooks:
  name_of_webhook:
    url: https://discord.com/...
    subs:  # List of feeds
      - feed_just_link
      - my_blog
```

## Build Index, No Spam
If you just want to create an index of existing posts to avoid spamming, use the command below.
It will run a script once that just downloads the feeds and creates an index.
Then, you can run it, and anything new that isn't in the index will be posted.

## Prepare

Make empty file for volume.

```bash
touch memory.msgpack
docker-compose run app python main.py --only-build-memory
```

# TODO
- [x] Encapsulate the code in main.py in the Rss2Discord package to clean up main.py
- [ ] Add timestamps to the memory so that it can be cleaned up. Currently, the memory will always increase in size.