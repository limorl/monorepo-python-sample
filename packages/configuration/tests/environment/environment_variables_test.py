import os
import unittest
from configuration.environment.environment_variables import EnvironmentVariables, Platform, Environment, reset_environment_variables


class TestEnvironmentVariables(unittest.TestCase):
    def setUp(self):
        reset_environment_variables()

    def test_init_environment_variables_dev_env(self):
        os.environ['PLATFORM'] = 'local'
        os.environ['ENVIRONMENT'] = 'dev'
        os.environ['CLOUD_ENDPOINT_OVERRIDE'] = 'http://localhost:4566'
        env = EnvironmentVariables()
       
        self.assertEqual(env.platform, Platform.LOCAL)
        self.assertEqual(env.cloud_endpoint_override, 'http://localhost:4566')
        self.assertEqual(env.environment, Environment.DEV)
    
    def test_init_environment_variables_prod_env(self):
        os.environ['PLATFORM'] = 'AWS'
        os.environ['REGION'] = 'east-us-1'
        os.environ['ENVIRONMENT'] = 'prod'
        os.environ['SERVICE_NAME'] = 'hello'
        env = EnvironmentVariables()
       
        self.assertEqual(env.platform, Platform.AWS)
        self.assertEqual(env.region, 'east-us-1')
        self.assertEqual(env.service_name, 'hello')
        self.assertEqual(env.environment, Environment.PROD)
    
    def test_init_environment_variables_empty_env_should_not_fail(self):
        env = EnvironmentVariables()
       
        self.assertEqual(env.platform, None)
        self.assertEqual(env.region, None)
        self.assertEqual(env.service_name, None)
        self.assertEqual(env.cloud_endpoint_override, None)
        self.assertEqual(env.local_configuration_folder, None)
        self.assertEqual(env.environment, None)

    def test_init_environment_variables_dev_dotenv_path(self):
        dotnev_path = os.path.join(os.getcwd(), 'tests/__data__/.dev.env')
        env = EnvironmentVariables(dotnev_path)
       
        self.assertEqual(env.platform, Platform.LOCAL)
        self.assertEqual(env.cloud_endpoint_override, 'http://localhost:4566')
        self.assertEqual(env.service_name, 'hello')
        self.assertEqual(env.environment, Environment.DEV)
    

    def test_init_environment_variables_prod_dotenv_path(self):
        dotnev_path = os.path.join(os.getcwd(), 'tests/__data__/.prod.env')
        env = EnvironmentVariables(dotnev_path)
       
        self.assertEqual(env.platform, Platform.AWS)
        self.assertEqual(env.region, 'east-us-1')
        self.assertEqual(env.service_name, 'hello')
        self.assertEqual(env.environment, Environment.PROD)

    
    def test_init_environment_variables_empty_dotenv_path(self):
        dotnev_path = os.path.join(os.getcwd(), 'tests/__data__/.empty.env')
        env = EnvironmentVariables(dotnev_path)
       
        self.assertEqual(env.platform, None)
        self.assertEqual(env.region, None)
        self.assertEqual(env.service_name, None)
        self.assertEqual(env.cloud_endpoint_override, None)
        self.assertEqual(env.local_configuration_folder, None)
        self.assertEqual(env.environment, None)

    
    def test_init_environment_variables_unknown_platform_should_throw(self):
        dotnev_path = os.path.join(os.getcwd(), 'tests/__data__/.unknown.platform.env')
        self.assertRaises(ValueError, EnvironmentVariables, dotnev_path)

    
    def test_init_environment_variables_unknown_environment_should_throw(self):
        dotnev_path = os.path.join(os.getcwd(), 'tests/__data__/.unknown.environment.env')
        self.assertRaises(ValueError, EnvironmentVariables, dotnev_path)

if __name__ == '__main__':
    unittest.main()
