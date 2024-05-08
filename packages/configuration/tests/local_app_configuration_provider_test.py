import os
import pytest
from configuration.local_app_configuration_provider import LocalAppConfigurationProvider
from environment.environment_variables import EnvironmentVariables, reset_environment_variables


@pytest.fixture()
def reset_env():
    reset_environment_variables()
    config_folder = os.path.join(os.getcwd(), 'tests/config')
    os.environ['LOCAL_CONFIGURATION_FOLDER'] = config_folder


def test_get_raw_configuration_dev(reset_env):
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    env_variables = EnvironmentVariables()
    app_config_provider = LocalAppConfigurationProvider(env_variables)
    app_config_provider.init_configuration()

    assert app_config_provider.get_configuration('raw1') == 1
    assert app_config_provider.get_configuration('raw2') == 2


def test_get_configuration_section_dev(reset_env):
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'

    env_variables = EnvironmentVariables()
    app_config_provider = LocalAppConfigurationProvider(env_variables)

    app_config_provider.init_configuration()
    config1 = app_config_provider.get_configuration('section1')
    config10 = app_config_provider.get_configuration('section10')

    assert config1['num1'] == 1
    assert config1['str1'] == 'val1'
    assert config10['num10'] == 10
    assert config10['str10'] == 'val10'


def test_get_raw_configuration_prod(reset_env):
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-east-1'
    os.environ['SERVICE_NAME'] = 'hello'

    env_variables = EnvironmentVariables()
    app_config_provider = LocalAppConfigurationProvider(env_variables)
    app_config_provider.init_configuration()

    assert app_config_provider.get_configuration('raw100') == 100
    assert app_config_provider.get_configuration('raw200') == 200


def test_get_configuration_section_prod(reset_env):
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-east-1'
    os.environ['SERVICE_NAME'] = 'hello'

    env_variables = EnvironmentVariables()
    app_config_provider = LocalAppConfigurationProvider(env_variables)

    app_config_provider.init_configuration()
    config = app_config_provider.get_configuration('section100')

    assert config['num100'] == 100
    assert config['str200'] == '200'


def test_get_configuration_section_prod_missing_service_name_should_throw_value_error(reset_env):
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-east-1'

    with pytest.raises(ValueError) as exc_info:
        EnvironmentVariables()

    assert "Missing service name" in str(exc_info.value)
