from pydantic import BaseModel
import yaml


class Hook(BaseModel):
    url: str
    subs: list[str]


def parse_yaml(file: str) -> dict[str, Hook]:
    with open(file) as f:
        root: dict = yaml.safe_load(f)

    hooks = {}
    for hook, data in (root.get('webhooks') or {}).items():
        hooks[hook] = Hook.model_validate(data)

    return hooks