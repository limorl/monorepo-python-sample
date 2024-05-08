import os
from unittest.mock import Mock
import pytest

from greeting.app import create_app, GreetingService
from environment.environment_variables import reset_environment_variables

@pytest.fixture(params=[2, 5, 0])
def mock_config_provider(request):
    mock_config_provider = Mock()
    mock_config_provider.get_configuration.return_value = request.param
    return mock_config_provider

@pytest.fixture
def app(mock_config_provider):
    reset_environment_variables()
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    greeting_service = GreetingService()

    # Create the app with the mocked configuration provider
    app = create_app(mock_config_provider, greeting_service)
    app.testing = True

    return app

def test_hello_name(app, mock_config_provider):
    num_exclamations = mock_config_provider.get_configuration()
    expected_greeting = f'Hello John{"!"*num_exclamations}'

    with app.test_client() as client:
        response = client.get('/hello/John')
        
        assert response.status_code == 200
        assert expected_greeting in response.get_data(as_text=True)