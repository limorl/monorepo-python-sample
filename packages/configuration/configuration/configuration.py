from typing import Any, Dict, TypeVar


class Configuration:
    def __init__(self):
        pass


# Generic type for any object extending Configuration
ConfigT = TypeVar('ConfigT', bound=Configuration)


ConfigurationSection = Dict[str, Any]
