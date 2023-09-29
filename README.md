# Rss2Discord

Statically configured job that regularly crawls set RSS feeds and sends them to set Discord webhooks.

Configuration example:
```yaml
# Feed conf
rss:
  feed_just_link: https://blog1.website.net/rss
  my_blog:
    url: https://blog.my-site.org/feed
    color: 0xefd613  # Hex value of embeds for this feed, default val
    simple_link: no  # If set to yes, then only links are sent (so that Discord will load the embed from the link), so they are plain text messages.
    interval: null   # For overwrite crawl check interval, in minutes, minimum is 10 minutes

# Hooks conf
webhooks:
  name_of_webhook:
    url: https://discord.com/...
    subs:  # List of feeds
      - feed_just_link
      - my_blog
```

## Build index, no spam

If you just want to create an index of existing posts to avoid spamming, then you can use the command below.
It will run a script once that just downloads the feeds and creates an index.
Then you can run it and anything new that isn't in the index will be posted.

`docker run rss2discord_app python main.py --only-build-memory`


# TODO

- [ ] Encapsulate the code in main.py in the Rss2Discord package to clean up main.py
- [ ] Add timestamps to the memory so that the memory can be cleaned. Currently it will always increment the size.