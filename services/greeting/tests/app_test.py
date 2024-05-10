import os
from unittest.mock import Mock
import pytest
from greeting.greeting import Greeting
from greeting.app import create_app
from greeting.greeting_configuration import GreetingConfiguration
from environment.environment_variables import reset_environment_variables


@pytest.fixture(params=[2, 5, 0])
def mock_config_provider(request):
    mock_config_provider = Mock()
    greetign_configuration = GreetingConfiguration({'num_of_exclamations': request.param})
    mock_config_provider.get_configuration.return_value = greetign_configuration
    return mock_config_provider


@pytest.fixture
def app(mock_config_provider):
    reset_environment_variables()
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    greeting_service = Greeting(mock_config_provider)

    app = create_app(mock_config_provider, greeting_service)
    app.testing = True

    return app


def test_hello(app, mock_config_provider):
    greeting_configuration: GreetingConfiguration = mock_config_provider.get_configuration(GreetingConfiguration)
    expected_greeting = f'Hello {"!" * greeting_configuration.num_of_exclamations}'

    with app.test_client() as client:
        response = client.get('/hello')

        assert response.status_code == 200
        assert expected_greeting in response.get_data(as_text=True)


def test_hello_name(app, mock_config_provider):
    greeting_configuration: GreetingConfiguration = mock_config_provider.get_configuration(GreetingConfiguration)
    expected_greeting = f'Hello John{"!" * greeting_configuration.num_of_exclamations}'

    with app.test_client() as client:
        response = client.get('/hello/John')

        assert response.status_code == 200
        assert expected_greeting in response.get_data(as_text=True)
