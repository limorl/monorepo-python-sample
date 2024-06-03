import contextlib
import os
from typing import Any

from configuration.configuration import Configuration
from configuration.configuration_provider import IConfigurationProvider
from flask import Flask

from greeting.greeting import IGreeting
from greeting.lambda_logging import get_lambda_logger

logger = get_lambda_logger()


class AppConfiguration(Configuration):
    def __init__(self, data: dict):
        self.html_heading: str = data['html_heading']


def create_app(config_provider: IConfigurationProvider, greeting: IGreeting) -> Any:
    app = Flask(__name__, instance_relative_config=True)
    config = config_provider.get_configuration(AppConfiguration)

    with contextlib.suppress(OSError):
        os.makedirs(app.instance_path, exist_ok=True)

    @app.route('/hello')
    def hello() -> str:
        if config and config.html_heading:
            return f'<{config.html_heading}>{greeting.hello()}</{config.html_heading}>'
        return greeting.hello()

    @app.route('/hello/<name>')
    def hello_name(name: str) -> str:
        if config and config.html_heading:
            return f'<{config.html_heading}>{greeting.hello(name)}</{config.html_heading}>'
        return greeting.hello(name)

    return app
