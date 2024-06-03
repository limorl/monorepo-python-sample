import json
import logging
import os
from typing import Any

from environment.service_environment import ServiceEnvironment, is_cloud_platform

from configuration.configuration import Configuration, ConfigurationSection
from configuration.configuration_provider import IConfigurationProvider
from configuration.secret import is_secret, parse_secret_value, try_get_secret_name

logger = logging.getLogger()


class LocalConfigurationProvider(IConfigurationProvider):
    """ Local Configuration Provider.
        Provides configuration based on local configuration file and Environment Variables"""
    _service_env: ServiceEnvironment = None
    _config_file_path: str = ''

    def __init__(self, service_env: ServiceEnvironment):
        super().__init__()

        self._service_env = service_env
        self._config_file_path = self._get_config_file_path()

        logger.debug(f"LocalConfigurationProvider _local_config_path set to: {self._config_file_path}")

    def get_configuration[T: Configuration](self, config_type: type[T]) -> T:  # pylint: disable=invalid-syntax
        return super().get_configuration(config_type)

    def _read_configuration(self) -> dict[str, ConfigurationSection]:
        try:
            with open(self._config_file_path) as file:
                logger.debug(f"LocalConfigurationProvider loading configuration file: {self._config_file_path}")
                configuration_dict: dict[str, Any] = json.load(file)
                configuration_with_secrets: dict[str, ConfigurationSection] = {}

                for key, val in configuration_dict.items():
                    configuration_with_secrets[key] = self._populate_secrets(val)

                return configuration_with_secrets
        except FileNotFoundError:
            logger.exception(f"Configuration file not found: {self._config_file_path}")
            return None
        except json.JSONDecodeError:
            logger.exception(f"Failed to decode JSON from configuration: {self._config_file_path}")
            return None

    def _get_config_file_path(self) -> str:
        default_config_folder = os.path.join(os.getcwd(), 'config')
        local_config_folder = self._service_env.local_configuration_folder or default_config_folder

        platform = self._service_env.platform.value.lower()
        stage = self._service_env.stage.value.lower()
        region = self._service_env.region

        if is_cloud_platform(self._service_env.platform):
            return os.path.join(local_config_folder, f'{platform}.{stage}.{region}.json')
        return os.path.join(local_config_folder, f'{platform}.{stage}.json')

    def _populate_secrets(self, config: dict[str, Any]) -> dict[str, Any]:
        config_with_secrets = {}

        for key, val in config.items():
            if is_secret(val):
                secret_name = try_get_secret_name(val)
                config_with_secrets[key] = parse_secret_value(os.environ[secret_name])
            elif isinstance(val, dict) and not isinstance(val, list):
                config_with_secrets[key] = self._populate_secrets(val)
            else:
                config_with_secrets[key] = val

        return config_with_secrets
