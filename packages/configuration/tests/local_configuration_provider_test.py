import os
import pytest
import pathlib
from configuration.configuration import Configuration, ConfigurationDict
from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.environment_variables import EnvironmentVariables, reset_environment_variables


@pytest.fixture()
def reset_env():
    reset_environment_variables()
    config_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'config')
    os.environ['LOCAL_CONFIGURATION_FOLDER'] = config_folder


class TestConfiguration1(Configuration):
    def __init__(self, config_dict: ConfigurationDict):
        self.int100 = config_dict['int100']
        self.int200 = config_dict['int200']
        self.section100 = config_dict.get('section100', {})


class TestConfiguration2(Configuration):

    def __init__(self, config_dict: ConfigurationDict):
        self.int1 = config_dict.get('int1')
        self.int2 = config_dict.get('int2')
        self.section1 = config_dict.get('section1', {})
        self.section10 = config_dict.get('section10', {})


@pytest.mark.asyncio
async def test_get_configuration_local_dev(reset_env):
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    env_variables = EnvironmentVariables()
    config_provider = LocalConfigurationProvider(env_variables)
    await config_provider.init_configuration()

    config: TestConfiguration2 = config_provider.get_configuration(TestConfiguration2)

    assert config.int1 == 1
    assert config.int1 == 1
    assert config.int2 == 2
    assert config.section1.get('int1') == 1
    assert config.section1.get('str1') == '1'
    assert config.section10.get('int10') == 10
    assert config.section10.get('str10') == '10'


@pytest.mark.asyncio
async def test_get_configuration_aws_prod(reset_env):
    os.environ['PLATFORM'] = 'aws'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-east-1'
    os.environ['SERVICE_NAME'] = 'hello'

    env_variables = EnvironmentVariables()
    config_provider = LocalConfigurationProvider(env_variables)
    await config_provider.init_configuration()

    config: TestConfiguration1 = config_provider.get_configuration(TestConfiguration1)

    assert config.int100 == 100
    assert config.int200 == 200
    assert config.section100.get('str100') == '100'
    assert config.section100.get('str200') == '200'
