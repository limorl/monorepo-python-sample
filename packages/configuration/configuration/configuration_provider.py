import json
import os
from abc import ABC, abstractmethod
from typing import Any


class IConfigurationProvider(ABC):
    @abstractmethod
    def get_config(self, key: str) -> Any:
        """Retrieves the value of a configuration setting by key."""
        pass


class LocalConfigurationProvider(IConfigurationProvider):
    def __init__(self):
        self.config = {}
        # config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.local.json')
        config_path = os.path.join(os.getcwd(), 'config/config.local.json')
        print("config path (local): ", config_path)
        print("cwd path: ", os.getcwd())
        print("dir(file): ", os.path.dirname(__file__))

        with open(config_path, 'r') as file:
            self.config = json.load(file)

    def get_config(self, key: str) -> str:
        return self.config.get(key, '')


class AppConfigurationProvider(IConfigurationProvider):
    def __init__(self):
        self.config = {}
        # config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config/config.prod.us-east-1.json')
        config_path = os.path.join(os.getcwd(), 'config/config.prod.us-east-1.json')

        with open(config_path, 'r') as file:
            self.config = json.load(file)

    def get_config(self, key: str) -> str:
        return self.config.get(key, '')


def get_configuration_provider() -> IConfigurationProvider:
    """Determines and returns the appropriate configuration provider."""
    environment = os.getenv('ENVIRONMENT', 'Local')
    if environment == 'Local':
        return LocalConfigurationProvider()
    else:
        return AppConfigurationProvider()
