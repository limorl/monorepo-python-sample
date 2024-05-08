from unittest.mock import Mock
from hello_world.app import lambda_handler


def test_hello_world():
    event = Mock()
    context = Mock()

    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert response['body'] == '"Hello World!"'
