import os
import unittest
from configuration.app.local_configuration_provider import LocalConfigurationProvider
from configuration.environment.environment_variables import EnvironmentVariables, reset_environment_variables


class TestLocalConfigurationProvider(unittest.TestCase):
    def setUp(self):
        reset_environment_variables()
        os.environ['LOCAL_CONFIGURATION_FOLDER'] = os.path.join(os.getcwd(), 'tests/__data__/config')

    def test_get_raw_configuration_dev(self):
        os.environ['PLATFORM'] = 'local'
        os.environ['STAGE'] = 'dev'
        env_variables = EnvironmentVariables()

        config_provider = LocalConfigurationProvider(env_variables)
        config_provider.init_configuration()
        val1 = config_provider.get_configuration('raw1')
        val2 = config_provider.get_configuration('raw2')

        self.assertEqual(val1, 1)
        self.assertEqual(val2, 2)

    def test_get_configuration_section_dev(self):
        os.environ['PLATFORM'] = 'local'
        os.environ['STAGE'] = 'dev'
        env_variables = EnvironmentVariables()
        config_provider = LocalConfigurationProvider(env_variables)

        config_provider.init_configuration()
        config1 = config_provider.get_configuration('section1')
        config10 = config_provider.get_configuration('section10')

        self.assertEqual(config1['num1'], 1)
        self.assertEqual(config1['str1'], 'val1')
        self.assertEqual(config10['num10'], 10)
        self.assertEqual(config10['str10'], 'val10')

    def test_get_raw_configuration_prod(self):
        os.environ['PLATFORM'] = 'AWS'
        os.environ['STAGE'] = 'prod'
        os.environ['REGION'] = 'east-us-1'
        os.environ['SERVICE_NAME'] = 'hello'
        env_variables = EnvironmentVariables()

        config_provider = LocalConfigurationProvider(env_variables)
        config_provider.init_configuration()
        val1 = config_provider.get_configuration('raw100')
        val2 = config_provider.get_configuration('raw200')

        self.assertEqual(val1, 100)
        self.assertEqual(val2, 200)

    def test_get_configuration_section_prod(self):
        os.environ['PLATFORM'] = 'AWS'
        os.environ['STAGE'] = 'prod'
        os.environ['REGION'] = 'east-us-1'
        os.environ['SERVICE_NAME'] = 'hello'
        env_variables = EnvironmentVariables()
        config_provider = LocalConfigurationProvider(env_variables)

        config_provider.init_configuration()
        config = config_provider.get_configuration('section100')

        self.assertEqual(config['num100'], 100)
        self.assertEqual(config['str200'], '200')

    def test_get_configuration_section_prod_missing_service_name_should_throw_value_error(self):
        os.environ['PLATFORM'] = 'AWS'
        os.environ['STAGE'] = 'prod'
        os.environ['REGION'] = 'east-us-1'

        self.assertRaises(ValueError, EnvironmentVariables)


if __name__ == '__main__':
    unittest.main()
