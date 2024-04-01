import os
from .greeting_service import GreetingService
from .configuration_provider import IConfigurationProvider, get_configuration_provider
from flask import Flask


def create_app(configProvider: IConfigurationProvider):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    greeting = GreetingService()
    numOfExclamations = configProvider.get_config('numOfExclamations')

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

    @app.route('/bye')
    def bye():
        # Says bye !!
        return greeting.bye('', numOfExclamations)

    return app


config_provider = get_configuration_provider()
app = create_app(config_provider)
