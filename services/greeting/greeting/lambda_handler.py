from configuration.configuration_provider import IConfigurationProvider
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.environment_variables import EnvironmentVariables, Platform
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
    env_variables = EnvironmentVariables()
    logger.debug(f"greeting-service app created with env_variables: {env_variables}")

    config_provider: IConfigurationProvider = None

    if env_variables.platform == Platform.LOCAL:
        config_provider = LocalConfigurationProvider(env_variables)
    else:
        # TODO: Implement AppConfigConfigurationProvider using AWS AppConfig and then uncomment instead of LocalConfigurationProvider
        # config_provider = AppConfigConfigurationProvider()
        config_provider = LocalConfigurationProvider(env_variables)

    config_provider.init_configuration()
    return config_provider
