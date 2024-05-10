from typing import Any, Dict, TypeVar


class Configuration:
    def __init__(self):
        pass


ConfigurationDict = Dict[str, Any]

ConfigT = TypeVar('ConfigT', bound=Configuration)
