import unittest
from unittest.mock import Mock
from hello_world.app import lambda_handler


class TestHelloWorldLambda(unittest.TestCase):
    def test_hello_world(self):
        event = Mock()
        context = Mock()

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], '"Hello World!"')


if __name__ == '__main__':
    unittest.main()
