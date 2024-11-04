from bs4 import BeautifulSoup

from Rss2Discord.Models import Hook


def revert_feeds_to_hooks(hooks: dict[str, Hook]):
    reverted: dict[str, list[str]] = {}

    for key, hook in hooks.items():
        for sub in hook.subs:
            reverted.setdefault(sub, []).append(hook.url)

    return reverted


def drop_html_tags(string):
    soup = BeautifulSoup(string, "html.parser")

    for tag in soup.find_all(True):
        tag.decompose()

    return soup.get_text()


def unwrap_html_tags(string):
    soup = BeautifulSoup(string, "html.parser")

    for tag in soup.find_all(True):
        tag.unwrap()

    return soup.get_text()
