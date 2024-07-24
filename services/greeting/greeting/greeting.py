from abc import ABC, abstractmethod

from configuration.configuration_provider import IConfigurationProvider

from .greeting_configuration import GreetingConfiguration


class IGreeting(ABC):
    @abstractmethod
    def hello(self, name: str = '') -> str:
        pass


class Greeting(IGreeting):
    def __init__(self, config_provider: IConfigurationProvider):
        self._config = config_provider.get_configuration(GreetingConfiguration)

    def hello(self, name: str = '') -> str:
        return f"Hi {name}{'!' * self._config.num_of_exclamations}"
