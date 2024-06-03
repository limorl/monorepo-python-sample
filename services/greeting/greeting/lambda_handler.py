from typing import Any

from configuration.app_config_configuration_provider import AppConfigConfigurationProvider
from configuration.configuration_provider import IConfigurationProvider
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.service_environment import Platform, ServiceEnvironment
from serverless_wsgi import handle_request

from greeting.app import create_app
from greeting.greeting import Greeting
from greeting.lambda_logging import get_lambda_logger

logger = get_lambda_logger()


def handler(event: dict, context: dict) -> Any:
    configuration_provider = create_and_init_configuration_provider()
    app = create_app(configuration_provider, Greeting(configuration_provider))

    return handle_request(app, event, context)


def create_and_init_configuration_provider() -> IConfigurationProvider:
    service_env = ServiceEnvironment()
    logger.debug(f"greeting-service created with service environment: {service_env}")

    config_provider: IConfigurationProvider = None

    if service_env.platform == Platform.LOCAL:
        config_provider = LocalConfigurationProvider(service_env)
        logger.info(f'Service {service_env.service_name} initialized with LocalConfigurationProvider')

    else:
        config_provider = AppConfigConfigurationProvider(service_env)
        logger.info(f'Service {service_env.service_name} initialized with AppConfigurationProvider')

    config_provider.init_configuration()
    return config_provider
