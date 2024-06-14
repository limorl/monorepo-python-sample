import os
import pytest
import pathlib
from configuration.app_config_utils import app_config_deploy_service_configuration
from configuration.app_config_configuration_provider import AppConfigConfigurationProvider
from configuration.configuration_provider import ConfigurationSection
from configuration.configuration import Configuration
from environment.service_environment import ServiceEnvironment, clear_service_environment, restore_local_dev_service_environment


class GooConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):
        self.int1 = config_dict['int1']
        self.str2 = config_dict['str2']
        self.secrets = config_dict.get('secrets', {})


@pytest.fixture
def configuration():
    return GooConfiguration({
        'int1': 1,
        'str2': '2',
        'secrets': {
            'secret_plain': 'secret:test/app/fake-secret-plain',
            'secret_pair': 'secret:test/app/fake-secret-pair'
        }
    })


@pytest.fixture
def configuration_with_populated_secrets():
    return GooConfiguration({
        'int1': 1,
        'str2': '2',
        'secrets': {
            'secret_plain': 'fake-secret-val',
            'secret_pair': {
                'Username': 'fake-username',
                'Password': 'fake-password'
            }
        }
    })


@pytest.fixture
def service_env():
    clear_service_environment()
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'dev'
    os.environ['REGION'] = 'us-west-2'
    os.environ['SERVICE_NAME'] = 'test-appconfig'

    config_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'config')
    os.environ['LOCAL_CONFIGURATION_FOLDER'] = config_folder

    yield ServiceEnvironment()
    restore_local_dev_service_environment()


@pytest.fixture
def app_configuration_provider(service_env):
    app_configuration_provider = AppConfigConfigurationProvider(service_env)
    app_configuration_provider.init_configuration()
    return app_configuration_provider


""" This test assumes the following resources exists in Dev/Test env:

    Test.Linear.AllatOnce configuration deployment strategy (all at once with duration 0 and bake time 0)

    Two secrets are stored on Secretes Manager:
    - Plain text secret: 'test/app/fake-secret-plain' = fake-secret-val
    - Key/Value secret: 'secret:test/app/fake-secret-pair': {
                'Username': 'fake-username',
                'Password': 'fake-password'
            }

    TODO (@limorl): Test can be imprived to deploy a newly created configuration and then deleted after test test
"""


@pytest.mark.integration
def test_init_and_get_configuration__success(
    service_env,
    configuration_with_populated_secrets,
):
    app_config_deploy_service_configuration(service_env.service_name, service_env.platform, service_env.stage, service_env.region, None, service_env.local_configuration_folder)

    app_configuration_provider = AppConfigConfigurationProvider(service_env)
    app_configuration_provider.init_configuration()

    configuration: GooConfiguration = app_configuration_provider.get_configuration(GooConfiguration)

    assert configuration
    assert configuration.int1 == configuration_with_populated_secrets.int1
    assert configuration.str2 == configuration_with_populated_secrets.str2
    assert configuration.secrets['secret_plain'] == configuration_with_populated_secrets.secrets['secret_plain']
    assert configuration.secrets['secret_pair']['Username'] == configuration_with_populated_secrets.secrets['secret_pair']['Username']
    assert configuration.secrets['secret_pair']['Password'] == configuration_with_populated_secrets.secrets['secret_pair']['Password']
