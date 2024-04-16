import unittest
from unittest.mock import Mock
import os
from greeting.app import create_app, GreetingService
from configuration.environment.environment_variables import reset_environment_variables


class TestLambdaFunction(unittest.TestCase):
    def setUp(self):
        reset_environment_variables()
        os.environ['PLATFORM'] = 'local'
        os.environ['ENVIRONMENT'] = 'dev'

    def test_hello_name(self):
        # Create a mock configuration provider
        mock_config_provider = Mock()
        mock_config_provider.get_configuration.return_value = 2  # Mock return value for numOfExclamations
        greeting_service = GreetingService()

        # Create the app with the mocked configuration provider
        test_app = create_app(mock_config_provider, greeting_service)
        test_app.testing = True
        with test_app.test_client() as client:
            # Make a test request to the hello_name endpoint
            response = client.get('/hello/John')
            self.assertEqual(response.status_code, 200)

            # Check if the response contains the expected greeting
            expected_greeting = 'Hello John!!'  # Expecting 2 exclamation marks as mocked
            self.assertIn(expected_greeting, response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
