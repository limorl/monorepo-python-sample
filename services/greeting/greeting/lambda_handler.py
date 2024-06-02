from configuration.configuration_provider import IConfigurationProvider
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.service_environment import ServiceEnvironment, Platform
from greeting.lambda_logging import get_lambda_logger
from greeting.app import create_app
from greeting.greeting import Greeting
from serverless_wsgi import handle_request


logger = get_lambda_logger()


def handler(event, context):
    configuration_provider = create_and_init_configuration_provider()
    app = create_app(configuration_provider, Greeting(configuration_provider))

    return handle_request(app, event, context)


def create_and_init_configuration_provider() -> IConfigurationProvider:
    service_env = ServiceEnvironment()
    logger.debug(f"greeting-service created with service environment: {service_env}")

    config_provider: IConfigurationProvider = None

    if service_env.platform == Platform.LOCAL:
        config_provider = LocalConfigurationProvider(service_env)
    else:
        # TODO: Implement AppConfigConfigurationProvider using AWS AppConfig and then uncomment instead of LocalConfigurationProvider
        # config_provider = AppConfigConfigurationProvider()
        config_provider = LocalConfigurationProvider(service_env)

    config_provider.init_configuration()
    return config_provider
