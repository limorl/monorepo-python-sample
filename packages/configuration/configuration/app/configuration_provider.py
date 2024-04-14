from abc import ABC, abstractmethod
from typing import Any


class IConfigurationProvider(ABC):
    _config: Any = {}

    @abstractmethod
    def init_configuration(self):
        pass

    @abstractmethod
    def get_configuration(self, key: str) -> Any:
        """Retrieves the value of a configuration setting by key."""
        return self._config.get(key, '')
