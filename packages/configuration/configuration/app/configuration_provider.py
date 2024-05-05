import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger()


class IConfigurationProvider(ABC):
    __initiated = False
    __initiating = False
    __config: Any = {}

    @abstractmethod
    def init_configuration(self):
        if (self.__initiated or self.__initiating):
            return

        self.__initiating = True
        self.__config = self._load_configuration()
        self.__initiating = False
        self.__initiated = True

        logger.debug(f"init_configuration: __confg: {self.__config}")

    @abstractmethod
    def get_configuration(self, key: str) -> Any:
        """Retrieves the value of a configuration setting by key."""
        if not self.__initiated:
            raise RuntimeError('Configuration provider is not initiated.')

        config = self.__config.get(key, None)
        if not config:
            raise KeyError(f'Configuration ${key} was not found')

        return config

    @abstractmethod
    def _load_configuration(self) -> Any:
        pass
