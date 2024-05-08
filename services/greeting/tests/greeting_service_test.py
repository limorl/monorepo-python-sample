import pytest
from greeting.greeting_service import GreetingService


@pytest.fixture()
def greeting_service():
    return GreetingService()


@pytest.fixture(params=[2, 5, 0])
def num_of_exclamations(request):
    return request.param


def test_hello(greeting_service, num_of_exclamations):
    msg = greeting_service.hello('John', num_of_exclamations)
    expected = f'Hello John{"!" * num_of_exclamations}'

    assert msg == expected
