import logging
from typing import Any

import boto3
from environment.service_environment import ServiceEnvironment

from .app_config_utils import (
    app_config_data_get_latest_configuration,
    app_config_get_application_id,
    app_config_get_environment_id,
    app_config_get_profile_id,
    get_app_name,
    get_config_name,
)
from .configuration import Configuration, ConfigurationSection
from .configuration_provider import IConfigurationProvider
from .secret import is_secret
from .secrets_manager_utils import secrets_manager_get_secret_value

logger = logging.getLogger()


class AppConfigConfigurationProvider(IConfigurationProvider):
    """Configuration Provider based on AWS App Config.
    When deploying services, the configuration files under the service's /config folders are deployed to AppConfig.
    This implementation assumed a single configuration per { service_name, stage, region } where stage maps to
    AppConfig Environment.

    SERVICE_DEFAULT_DEPLOYMENT_STRATEGY = holds the name of the strategy already created on AppConfig

    If multiple environments are needed, the lambda template should be updated with additional parameters, such as:
    Parameters:
        AppConfigEnvironment:
            Description: AppConfig Environment id
            Type: String
        AppConfigConfigProfile:
            Description: AppConfig Configuration Profile id
            Type: String

    It is recommended to use lambda extensions for appconfig and secretsmanager as explained here:
    https://medium.com/@guidonebiolo/boost-your-serverless-apps-with-aws-lambda-extensions-and-appconfig-5d41808c74ce.
    For now, we use a simple implementation in which in each lambda invocation, the configuration and secrets are retrieved
    from appcofig and secretsmanager.
    """  # noqa: E501

    def __init__(self, service_env: ServiceEnvironment):
        super().__init__()

        options: dict = {'region_name': service_env.primary_region}

        if service_env.cloud_endpoint_override:
            options['endpoint_url'] = service_env.cloud_endpoint_override

        self._appconfig = boto3.client('appconfig', **options)
        self._appconfigdata = boto3.client('appconfigdata', **options)
        self._secretsmanager = boto3.client('secretsmanager', **options)

        self._app_name = get_app_name(service_env.service_name)
        self._config_name = get_config_name(service_env.platform, service_env.stage, service_env.region)
        self._service_env = service_env

    def get_configuration[T: Configuration](self, config_type: type[T]) -> T:  # pylint: disable=invalid-syntax
        return super().get_configuration(config_type)

    def _read_configuration(self) -> dict[str, ConfigurationSection]:
        app_id = app_config_get_application_id(self._appconfig, self._app_name)
        profile_id = app_config_get_profile_id(self._appconfig, app_id, self._config_name)
        env_id = app_config_get_environment_id(self._appconfig, app_id, self._service_env.stage.value)

        configuration_dict: dict[str, Any] = app_config_data_get_latest_configuration(
            self._appconfigdata, app_id, env_id, profile_id
        )

        configuration_with_secrets: dict[str, ConfigurationSection] = {}

        for key, val in configuration_dict.items():
            configuration_with_secrets[key] = self._populate_secrets(val)

        return configuration_with_secrets

    def _populate_secrets(self, config: dict[str, Any]) -> dict[str, Any]:
        config_with_secrets = {}

        for key, val in config.items():
            if is_secret(val):
                secret_value = secrets_manager_get_secret_value(self._secretsmanager, val)
                config_with_secrets[key] = secret_value
            elif isinstance(val, dict) and not isinstance(val, list):
                config_with_secrets[key] = self._populate_secrets(val)
            else:
                config_with_secrets[key] = val

        return config_with_secrets
