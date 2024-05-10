import asyncio
import os
from .lambda_logging import get_logger
from .greeting import IGreeting, Greeting
from configuration.configuration_provider import IConfigurationProvider
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.environment_variables import EnvironmentVariables, Platform
from .greeting_configuration import GreetingConfiguration
# from configuration.app.app_config_configuration_provider import AppConfigConfigurationProvider
from flask import Flask


logger = get_logger()


def create_app(configProvider: IConfigurationProvider, greeting: IGreeting):
    app = Flask(__name__, instance_relative_config=True)

    greeting = greeting

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return greeting.hello()

    @app.route('/hello/<name>')
    def hello_name(name):
        return greeting.hello(name)

    return app


async def create_and_init_configuration_provider_async() -> IConfigurationProvider:
    env_variables = EnvironmentVariables()
    logger.debug(f"greeting-service app created with env_variables: {env_variables}")

    config_provider: IConfigurationProvider = None

    if env_variables.platform == Platform.LOCAL:
        config_provider = LocalConfigurationProvider(env_variables)
    else:
        # TODO: Implement AppConfigConfigurationProvider using AWS AppConfig and then uncomment instead of LocalConfigurationProvider
        # config_provider = AppConfigConfigurationProvider()
        config_provider = LocalConfigurationProvider(env_variables)
    
    await config_provider.init_configuration()
    return config_provider


def create_and_init_configuration_provider() -> IConfigurationProvider:
    return asyncio.run(create_and_init_configuration_provider_async())

configuration_provider = create_and_init_configuration_provider()
app = create_app(configuration_provider, Greeting(configuration_provider))
