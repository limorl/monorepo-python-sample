import os
import pytest
import pathlib
from configuration.configuration import Configuration, ConfigurationSection
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.environment_variables import EnvironmentVariables, reset_environment_variables


@pytest.fixture()
def reset_env():
    reset_environment_variables()
    config_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'config')
    os.environ['LOCAL_CONFIGURATION_FOLDER'] = config_folder


class FooConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):
        self.int100 = config_dict['int100']
        self.int200 = config_dict['int200']
        self.section100 = config_dict.get('section100', {})


class BarConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):
        self.int1 = config_dict.get('int1')
        self.int2 = config_dict.get('int2')
        self.section1 = config_dict.get('section1', {})
        self.section10 = config_dict.get('section10', {})
        self.secrets = config_dict.get('secrets', {})


def test_get_configuration_local_dev_with_env_secrets(reset_env):
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'
    os.environ['SERVICE_NAME'] = 'hello'
    os.environ['FAKE_SECRET_PLAIN']='fake-secret'
    os.environ['FAKE_SECRET_PAIR']='{"username": "fake-user", "password": "fake-password"}'

    env_variables = EnvironmentVariables()
    config_provider = LocalConfigurationProvider(env_variables)
    config_provider.init_configuration()

    config: BarConfiguration = config_provider.get_configuration(BarConfiguration)

    # assert configuration is correct and secrets were populated
    assert config
    assert config.int1 == 1
    assert config.int2 == 2
    assert config.section1.get('int1') == 1
    assert config.section1.get('str1') == '1'
    assert config.section10.get('int10') == 10
    assert config.section10.get('str10') == '10'
    assert config.secrets.get('secret_plain') == 'fake-secret'
    assert config.secrets.get('secret_pair')['username'] == 'fake-user'
    assert config.secrets.get('secret_pair')['password'] == 'fake-password'


def test_get_configuration_local_dev_dotenv_secrets(reset_env):
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'
    os.environ['SERVICE_NAME'] = 'hello'

    dotenv_path = config_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), '.env.test')
    env_variables = EnvironmentVariables(dotenv_path)
    config_provider = LocalConfigurationProvider(env_variables)
    config_provider.init_configuration()

    config: BarConfiguration = config_provider.get_configuration(BarConfiguration)
    
    # assert configuration is correct and secrets were populated
    assert config
    assert config.int1 == 1
    assert config.int2 == 2
    assert config.section1.get('int1') == 1
    assert config.section1.get('str1') == '1'
    assert config.section10.get('int10') == 10
    assert config.section10.get('str10') == '10'
    assert config.secrets.get('secret_plain') == 'fake-secret'
    assert config.secrets.get('secret_pair')['username'] == 'fake-user'
    assert config.secrets.get('secret_pair')['password'] == 'fake-password'


def test_get_configuration_aws_prod(reset_env):
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-east-1'
    os.environ['SERVICE_NAME'] = 'hello'

    env_variables = EnvironmentVariables()
    config_provider = LocalConfigurationProvider(env_variables)
    config_provider.init_configuration()

    config: FooConfiguration = config_provider.get_configuration(FooConfiguration)

    assert config
    assert config.int100 == 100
    assert config.int200 == 200
    assert config.section100.get('str100') == '100'
    assert config.section100.get('str200') == '200'
