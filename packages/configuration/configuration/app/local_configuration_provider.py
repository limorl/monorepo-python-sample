import json
import os
from typing import Any
from configuration.app.configuration_provider import IConfigurationProvider
from configuration.environment.environment_variables import EnvironmentVariables, Platform, Environment


class LocalConfigurationProvider(IConfigurationProvider):
    """ Local Configuration Provider.
        Provides configuration based on local configuration file and Environment Variables"""

    def __init__(self, env_variables: EnvironmentVariables):
        super().__init__()
        
        self._env_variables = env_variables

        default_config_folder = os.path.join(os.getcwd(), 'config')
        local_config_folder = env_variables.local_configuration_folder or default_config_folder

        if env_variables.environment == Environment.DEV:
            self._local_config_path = os.path.join(local_config_folder, 'config.dev.json')
        elif env_variables.environment == Environment.PROD and env_variables.region:
            self._local_config_path = os.path.join(local_config_folder, f'config.prod.{env_variables.region}.json')
   

    def init_configuration(self):
        super().init_configuration()

    def get_configuration(self, key: str) -> Any:
        return super().get_configuration(key)
    
    def _get_configuration(self):
        print("*** LOCAL:: _init_configuration")
        try:
            with open(self._local_config_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Configuration file not found: {self._local_config_path}")
            return None
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from configuration: {self._local_config_path}")
            return None
