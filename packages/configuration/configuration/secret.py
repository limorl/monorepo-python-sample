import json
from typing import Any

SECRET_PREFIX = 'secret:'


def is_secret(val: str) -> bool:
    return isinstance(val, str) and val.startswith(SECRET_PREFIX)


def try_get_secret_name(val: str) -> str:
    if val and is_secret(val):
        return val.replace(SECRET_PREFIX, '')
    return None


def parse_secret_value(text: str) -> str | dict[str, Any]:
    try:
        if text and text.startswith('{') and text.endswith('}'):
            return json.loads(text)
    except ValueError:
        return None
    else:
        return text
