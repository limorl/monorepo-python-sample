import os
from .lambda_logging import get_logger
from .greeting_service import IGreetingService, GreetingService
from configuration.app_configuration_provider import IAppConfigurationProvider
from configuration.local_app_configuration_provider import LocalAppConfigurationProvider
from environment.environment_variables import EnvironmentVariables, Platform
# from configuration.app.app_config_configuration_provider import AppConfigConfigurationProvider
from flask import Flask

logger = get_logger()


def create_app(configProvider: IAppConfigurationProvider, greeting_service: IGreetingService):
    app = Flask(__name__, instance_relative_config=True)

    greeting = greeting_service
    config_provider.init_configuration()
    numOfExclamations = configProvider.get_configuration('numOfExclamations')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return greeting.hello('', numOfExclamations)

    @app.route('/hello/<name>')
    def hello_name(name):
        return greeting.hello(name, numOfExclamations)

    return app


env_variables = EnvironmentVariables()
logger.debug(f"greeting-service app created with env_variables: {env_variables}")

config_provider: IAppConfigurationProvider = None

if env_variables.platform == Platform.LOCAL:
    config_provider = LocalAppConfigurationProvider(env_variables)
else:
    # TODO: Implement AppConfigConfigurationProvider using AWS AppConfig and then uncomment instead of LocalConfigurationProvider
    # config_provider = AppConfigConfigurationProvider()
    config_provider = LocalAppConfigurationProvider(env_variables)

app = create_app(config_provider, GreetingService())
