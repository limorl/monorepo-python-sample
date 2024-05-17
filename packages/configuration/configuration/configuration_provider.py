import logging
from abc import ABC, abstractmethod
from typing import Dict, Type
from configuration.configuration import ConfigurationSection, ConfigT

logger = logging.getLogger()


class IConfigurationProvider(ABC):
    """ Synchronous Configuration Provider, initialized before creating apps (services) """

    __initiated = False
    __initiating = False
    __configuration: Dict[str, ConfigurationSection] = {}

    def init_configuration(self) -> None:
        if self.__initiated or self.__initiating:
            return

        self.__initiating = True
        self.__configuration = self._read_configuration()
        self.__initiating = False
        self.__initiated = True

        logger.debug(f"init_configuration: __config_dict: {self.__configuration}")

    def get_configuration(self, config_type: Type[ConfigT]) -> ConfigT:
        if not self.__initiated:
            raise RuntimeError('Configuration provider is not initiated.')

        config_data = self.__configuration.get(config_type.__name__, None)
        if not config_data:
            raise KeyError(f'Configuration ${config_type.__name__} was not found')

        return config_type(config_data)

    @abstractmethod
    def _read_configuration(self) -> Dict[str, ConfigurationSection]:
        pass
