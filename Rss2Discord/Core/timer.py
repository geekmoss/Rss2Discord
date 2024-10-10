from datetime import datetime, timedelta


class Timer:
    def __init__(self):
        self.mem = {}

    def get_interval(self, feed: str) -> float:
        """ Return minutes from last tick (crawl) """
        return (datetime.now() - self.mem.get(feed, datetime.now() - timedelta(days=1))).total_seconds() // 60

    def set_tick(self, feed: str):
        self.mem[feed] = datetime.now()
        return
