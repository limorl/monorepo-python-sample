import boto3
import logging
from typing import Dict, Type
from configuration.configuration import ConfigurationDict, ConfigT
from configuration.configuration_provider import IConfigurationProvider
from environment.environment_variables import EnvironmentVariables

logger = logging.getLogger()


class AppConfigConfigurationProvider(IConfigurationProvider):
    """TODO: Implement
    Configuration Provider based on AWS App Config.
    When deploying services, the configuration files under the service's /config folders are deployed"""

    def __init__(self, env_vars: EnvironmentVariables):
        super().__init__()

        options = {}
        if env_vars.cloud_endpoint_override:
            options['endpoint_url'] = env_vars.cloud_endpoint_override

        self._appconfig = boto3.client('appconfig', **options)
        self._ssm = boto3.client('ssm', **options)

        self._app_name = f'{env_vars.service_name}-{env_vars.stage}-{env_vars.region}'
        self._env_vars = env_vars

    def get_configuration(self, config_type: Type[ConfigT]) -> ConfigT:
        return super().get_configuration(config_type)

    def _read_configuration(self) -> Dict[str, ConfigurationDict]:
        pass
