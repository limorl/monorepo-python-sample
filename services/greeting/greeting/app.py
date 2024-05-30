import os
from greeting.lambda_logging import get_lambda_logger
from greeting.greeting import IGreeting
from configuration.configuration_provider import IConfigurationProvider
from flask import Flask


logger = get_lambda_logger()


def create_app(configProvider: IConfigurationProvider, greeting: IGreeting):
    app = Flask(__name__, instance_relative_config=True)

    greeting = greeting

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return greeting.hello()

    @app.route('/hello/<name>')
    def hello_name(name):
        return greeting.hello(name)

    return app
