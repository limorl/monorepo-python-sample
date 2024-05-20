import json
import logging
import os
from typing import Dict, Type
from configuration.configuration import ConfigurationSection, ConfigT
from configuration.configuration_provider import IConfigurationProvider
from environment.environment_variables import EnvironmentVariables, is_cloud_platform

logger = logging.getLogger()


class LocalConfigurationProvider(IConfigurationProvider):
    """ Local Configuration Provider.
        Provides configuration based on local configuration file and Environment Variables"""
    _env_variables = {}
    _config_file_path = ''

    def __init__(self, env_variables: EnvironmentVariables):
        super().__init__()

        self._env_variables = env_variables
        self._config_file_path = self._get_config_file_path()

        logger.debug(f"LocalConfigurationProvider _local_config_path set to: {self._config_file_path}")

    def get_configuration(self, config_type: Type[ConfigT]) -> ConfigT:
        return super().get_configuration(config_type)

    def _read_configuration(self) -> Dict[str, ConfigurationSection]:
        try:
            with open(self._config_file_path, 'r') as file:
                logger.debug(f"LocalConfigurationProvider loading configuration file: {self._config_file_path}")
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self._config_file_path}")
            return None
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON from configuration: {self._config_file_path}")
            return None

    def _get_config_file_path(self) -> str:
        default_config_folder = os.path.join(os.getcwd(), 'config')
        local_config_folder = self._env_variables.local_configuration_folder or default_config_folder

        platform = self._env_variables.platform.value.lower()
        stage = self._env_variables.stage.value.lower()
        region = self._env_variables.region

        if is_cloud_platform(self._env_variables.platform):
            return os.path.join(local_config_folder, f'{platform}.{stage}.{region}.json')
        else:
            return os.path.join(local_config_folder, f'{platform}.{stage}.json')
