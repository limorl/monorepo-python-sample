import pytest
from unittest.mock import Mock
from greeting.greeting import Greeting
from greeting.greeting_configuration import GreetingConfiguration


@pytest.fixture(scope="module", params=[2, 5, 0])
def greeting_configuration(request):
    return GreetingConfiguration({'num_of_exclamations': request.param})


@pytest.fixture(scope="module")
def mock_config_provider(greeting_configuration):
    mock_config_provider = Mock()
    mock_config_provider.get_configuration.return_value = greeting_configuration
    return mock_config_provider


@pytest.fixture(scope="module")
def greeting(mock_config_provider):
    return Greeting(mock_config_provider)


def test_hello(greeting, greeting_configuration):
    msg = greeting.hello()
    expected = f'Hi {"!" * greeting_configuration.num_of_exclamations}'

    assert msg == expected


def test_hello_name(greeting, greeting_configuration):
    msg = greeting.hello('John')
    expected = f'Hi John{"!" * greeting_configuration.num_of_exclamations}'

    assert msg == expected
