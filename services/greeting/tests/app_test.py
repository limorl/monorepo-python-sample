import os
from unittest.mock import Mock
import pytest
from greeting.app import create_app, GreetingService
from greeting.app_configuration import AppConfiguration
from environment.environment_variables import reset_environment_variables


@pytest.fixture(params=[2, 5, 0])
def mock_config_provider(request):
    mock_config_provider = Mock()
    app_configuration = AppConfiguration({ 'numOfExclamations': request.param })
    mock_config_provider.get_configuration.return_value = app_configuration
    return mock_config_provider


@pytest.fixture
def app(mock_config_provider):
    reset_environment_variables()
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    greeting_service = GreetingService()

    app = create_app(mock_config_provider, greeting_service)
    app.testing = True

    return app


def test_hello_name(app, mock_config_provider):
    app_configuration: AppConfiguration = mock_config_provider.get_configuration(AppConfiguration)
    expected_greeting = f'Hello John{"!" * app_configuration.numOfExclamations}'

    with app.test_client() as client:
        response = client.get('/hello/John')

        assert response.status_code == 200
        assert expected_greeting in response.get_data(as_text=True)
