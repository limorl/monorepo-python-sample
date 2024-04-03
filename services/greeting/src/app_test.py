import unittest
from unittest.mock import Mock
from .app import create_app


class TestLambdaFunction(unittest.TestCase):
    def test_hello_name_with_mock(self):
        # Create a mock configuration provider
        mock_config_provider = Mock()
        mock_config_provider.get_config.return_value = 2  # Mock return value for numOfExclamations

        # Create the app with the mocked configuration provider
        app = create_app(mock_config_provider)
        app.testing = True
        with app.test_client() as client:
            # Make a test request to the hello_name endpoint
            response = client.get('/hello/John')
            self.assertEqual(response.status_code, 200)

            # Check if the response contains the expected greeting
            expected_greeting = 'Hello John!!'  # Expecting 2 exclamation marks as mocked
            self.assertIn(expected_greeting, response.get_data(as_text=True))

    def test_hadar_greeting(self):
        # Create a mock configuration provider
        mock_config_provider = Mock()
        mock_config_provider.get_config.return_value = 1  # Mock return value for numOfExclamations

        # Create the app with the mocked configuration provider
        app = create_app(mock_config_provider)
        app.testing = True
        with app.test_client() as client:
            # Make a test request to the hello_name endpoint
            response = client.get('/hadar/there')
            self.assertEqual(response.status_code, 200)

            # Check if the response contains the expected greeting
            expected_greeting = 'Hadar says: Hello there!' 
            self.assertIn(expected_greeting, response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
