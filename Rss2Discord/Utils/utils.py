from Rss2Discord.Models import Hook


def revert_feeds_to_hooks(hooks: dict[str, Hook]):
    reverted: dict[str, list[str]] = {}

    for key, hook in hooks.items():
        for sub in hook.subs:
            reverted.setdefault(sub, []).append(hook.url)

    return reverted
