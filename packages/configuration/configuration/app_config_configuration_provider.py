import boto3
import logging
from typing import Dict, Type, List, Any
from environment.environment_variables import EnvironmentVariables
from .configuration import ConfigurationSection, ConfigT
from .configuration_provider import IConfigurationProvider
from .app_config_utils import compose_app_name, compose_config_name, app_config_get_application_id, app_config_get_profile_id, app_config_get_environment_id, app_config_data_get_latest_configuration
from .secrets_manager_utils import is_secret, secrets_manager_get_secret_value


logger = logging.getLogger()

# We are using app config on a single region, while services can be on multiple regions
APP_CONFIG_REGION = 'us-east-1'

class AppConfigConfigurationProvider(IConfigurationProvider):
    """ Configuration Provider based on AWS App Config.
        When deploying services, the configuration files under the service's /config folders are deployed to AppConfig.
        This implementation assumed a single configuration per { service_name, stage, region } where stage maps to AppConfig Environment
        DEFAULT_DEPLOYMENT_STRATEGY = holds the name of the strategy already created on AppConfig

        If multiple environments are needed, the lambda template should be updated with additional parameters, such as:
        Parameters:
            AppConfigEnvironment:
                Description: AppConfig Environment id
                Type: String
            AppConfigConfigProfile:
                Description: AppConfig Configuration Profile id
                Type: String

        It is recommended to use lambda extensions for appconfig and secretsmanager as explained here: https://medium.com/@guidonebiolo/boost-your-serverless-apps-with-aws-lambda-extensions-and-appconfig-5d41808c74ce.
        For now, we use a simple implementation in which in each lambda invocation, the configuration and secrets are retrieved from appcofig and secretsmanager.
    """

    def __init__(self, env_vars: EnvironmentVariables):
        super().__init__()

        options: Dict = {'region_name': APP_CONFIG_REGION}
        if env_vars.cloud_endpoint_override:
            options['endpoint_url'] = env_vars.cloud_endpoint_override

        self._appconfig = boto3.client('appconfig', **options)
        self._appconfigdata = boto3.client('appconfigdata', **options)
        self._secretsmanager = boto3.client('secretsmanager', **options)

        self._app_name = compose_app_name(env_vars.service_name)
        self._config_name = compose_config_name(env_vars.platform.value, env_vars.stage.value, env_vars.region)
        self._env_vars = env_vars

    def get_configuration(self, config_type: Type[ConfigT]) -> ConfigT:
        return super().get_configuration(config_type)

    def _read_configuration(self) -> Dict[str, ConfigurationSection]:
        app_id = app_config_get_application_id(self._appconfig, self._app_name)
        profile_id = app_config_get_profile_id(self._appconfig, app_id, self._config_name)
        env_id = app_config_get_environment_id(self._appconfig, app_id, self._env_vars.stage.value)

        configuration_dict: Dict[str, Any] = app_config_data_get_latest_configuration(self._appconfigdata, app_id, env_id, profile_id)

        configuration_with_secrets: Dict[str, ConfigurationSection] = {}

        for key, val in configuration_dict.items():
            configuration_with_secrets[key] = self._populate_secrets(val)

        return configuration_with_secrets

    def _populate_secrets(self, config: Dict[str, Any]) -> Dict[str, Any]:
        config_with_secrets = {}

        for key, val in config.items():
            if is_secret(val):
                secret_value = secrets_manager_get_secret_value(self._secretsmanager, val)
                config_with_secrets[key] = secret_value
            elif isinstance(val, dict) and not isinstance(val, List):
                config_with_secrets[key] = self._populate_secrets(val)
            else:
                config_with_secrets[key] = val

        return config_with_secrets
