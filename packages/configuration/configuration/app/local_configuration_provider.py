import json
import os
from typing import Any
from configuration.app.configuration_provider import IConfigurationProvider


class LocalConfigurationProvider(IConfigurationProvider):

    def __init__(self):
        super().__init__()
        default_config_folder = os.path.join(os.getcwd(), 'config')
        local_config_folder = os.getenv('LOCAL_CONFIGURATION_FOLDER') or default_config_folder

        self._local_config_path = os.path.join(local_config_folder, 'config.local.json')
        self.config = None


    def init_configuration(self):
        try:
            with open(self._local_config_path, 'r') as file:
                self._config = json.load(file)
        except FileNotFoundError:
            print(f"Configuration file not found: {self._local_config_path}")
            return None
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from configuration: {self._local_config_path}")
            return None


    def get_configuration(self, key: str) -> Any:
        return super().get_configuration(key)
