import asyncio
import os
from .lambda_logging import get_logger
from .greeting_service import IGreetingService, GreetingService
from configuration.configuration_provider import IConfigurationProvider
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.environment_variables import EnvironmentVariables, Platform
from .app_configuration import AppConfiguration
# from configuration.app.app_config_configuration_provider import AppConfigConfigurationProvider
from flask import Flask


logger = get_logger()


async def create_app_async(configProvider: IConfigurationProvider, greeting_service: IGreetingService):
    app = Flask(__name__, instance_relative_config=True)

    greeting = greeting_service
    await config_provider.init_configuration()
    config: AppConfiguration = configProvider.get_configuration(AppConfiguration)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return greeting.hello('', config.numOfExclamations)

    @app.route('/hello/<name>')
    def hello_name(name):
        return greeting.hello(name, config.numOfExclamations)

    return app


def create_app(configProvider: IConfigurationProvider, greeting_service: IGreetingService):
    return asyncio.run(create_app_async(configProvider, greeting_service))  # Run asynchronously


env_variables = EnvironmentVariables()
logger.debug(f"greeting-service app created with env_variables: {env_variables}")

config_provider: IConfigurationProvider = None

if env_variables.platform == Platform.LOCAL:
    config_provider = LocalConfigurationProvider(env_variables)
else:
    # TODO: Implement AppConfigConfigurationProvider using AWS AppConfig and then uncomment instead of LocalConfigurationProvider
    # config_provider = AppConfigConfigurationProvider()
    config_provider = LocalConfigurationProvider(env_variables)

app = create_app(config_provider, GreetingService())
