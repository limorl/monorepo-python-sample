import os
from unittest.mock import Mock
import pytest
from greeting.greeting import Greeting
from greeting.app import create_app, AppConfiguration
from greeting.greeting_configuration import GreetingConfiguration
from environment.service_environment import clear_service_environment


@pytest.fixture(params=[['h1', 2], ['h3', 5], ['', 0]])
def mock_config_provider(request):
    mock_config_provider = Mock()
    app_configuration = AppConfiguration({'html_headings': request.param[0]})
    greetign_configuration = GreetingConfiguration({'num_of_exclamations': request.param[1]})
    mock_config_provider.get_configuration.side_effect = (lambda type: app_configuration if type.__name__ == 'AppConfiguration' else greetign_configuration)
    return mock_config_provider


@pytest.fixture()
def app(mock_config_provider):
    clear_service_environment()
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    greeting_service = Greeting(mock_config_provider)

    app = create_app(mock_config_provider, greeting_service)
    app.testing = True

    return app


def test_hello(app, mock_config_provider):
    app_configuration: AppConfiguration = mock_config_provider.get_configuration(AppConfiguration)
    greeting_configuration: GreetingConfiguration = mock_config_provider.get_configuration(GreetingConfiguration)
    heading_start, heading_end = _get_heading_tags(app_configuration)

    expected_greeting = f'{heading_start}Hello {"!" * greeting_configuration.num_of_exclamations}{heading_end}'

    with app.test_client() as client:
        response = client.get('/hello')

        assert response.status_code == 200
        assert expected_greeting in response.get_data(as_text=True)


def test_hello_name(app, mock_config_provider):
    app_configuration: AppConfiguration = mock_config_provider.get_configuration(AppConfiguration)
    greeting_configuration: GreetingConfiguration = mock_config_provider.get_configuration(GreetingConfiguration)
    heading_start, heading_end = _get_heading_tags(app_configuration)

    expected_greeting = f'{heading_start}Hello John{"!" * greeting_configuration.num_of_exclamations}{heading_end}'

    with app.test_client() as client:
        response = client.get('/hello/John')

        assert response.status_code == 200
        assert expected_greeting in response.get_data(as_text=True)


def _get_heading_tags(app_configuration: AppConfiguration) -> tuple[str, str]:
    if app_configuration.html_headings:
        return f'<{app_configuration.html_headings}>', f'</{app_configuration.html_headings}>'
    return '', ''
