from abc import ABC, abstractmethod
from typing import Any


class IConfigurationProvider(ABC):
    __initiated = False
    __initiating = False
    __config: Any = {}

    @abstractmethod
    def init_configuration(self):
        if (self.__initiated or self.__initiating):
            return

        self.__initiating = True
        self.__config = self._get_configuration()
        self.__initiating = False
        self.__initiated = True

        print(f"init_configuration: __confg: {self.__config}")

    @abstractmethod
    def get_configuration(self, key: str) -> Any:
        """Retrieves the value of a configuration setting by key."""
        if not self.__initiated:
            raise RuntimeError('Configuration provider is not initiated.')

        print(f"get_configuration: __confg: {self.__config}")
        config = self.__config.get(key, None)
        if not config:
            raise KeyError(f'Configuration ${key} was not found')
        
        return config

    @abstractmethod
    def _get_configuration(self) -> Any:
        pass
