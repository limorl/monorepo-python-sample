import os
from .greeting_service import IGreetingService, GreetingService
from configuration.app.configuration_provider import IConfigurationProvider
from configuration.app.local_configuration_provider import LocalConfigurationProvider
from configuration.app.remote_configuration_provider import RemoteConfigurationProvider
from flask import Flask


def create_app(configProvider: IConfigurationProvider, greeting_service: IGreetingService):
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


environment = os.getenv('ENVIRONMENT', 'Local')
config_provider: IConfigurationProvider = None

if environment == 'Local':
    config_provider = LocalConfigurationProvider()

else:
    config_provider = RemoteConfigurationProvider()

app = create_app(config_provider, GreetingService())
