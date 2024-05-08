import json
import logging
import os
from typing import Any
from configuration.app_configuration_provider import IAppConfigurationProvider
from environment.environment_variables import EnvironmentVariables, Stage

logger = logging.getLogger()


class LocalAppConfigurationProvider(IAppConfigurationProvider):
    """ Local Configuration Provider.
        Provides configuration based on local configuration file and Environment Variables"""
    _env_variables = {}
    _local_config_path = ''

    def __init__(self, env_variables: EnvironmentVariables):
        super().__init__()

        self._env_variables = env_variables

        default_config_folder = os.path.join(os.getcwd(), 'config')
        local_config_folder = env_variables.local_configuration_folder or default_config_folder
        logger.debug(f"LocalConfigurationProvider _local_config_path set to: {self._local_config_path}")

        if env_variables.stage == Stage.DEV:
            self._local_config_path = os.path.join(local_config_folder, 'config.dev.json')
        elif env_variables.stage == Stage.PROD and env_variables.region:
            self._local_config_path = os.path.join(local_config_folder, f'config.prod.{env_variables.region}.json')


    def init_configuration(self):
        super().init_configuration()

    def get_configuration(self, key: str) -> Any:
        return super().get_configuration(key)

    def _load_configuration(self):
        try:
            with open(self._local_config_path, 'r') as file:
                logger.debug(f"LocalConfigurationProvider loading configuration file: {self._local_config_path}")
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self._local_config_path}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from configuration: {self._local_config_path}")
            return None
