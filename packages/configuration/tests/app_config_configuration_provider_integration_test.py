import os
import pytest
import pathlib
from configuration.app_config_configuration_provider import AppConfigConfigurationProvider
from configuration.configuration_provider import ConfigurationSection
from configuration.configuration import Configuration
from environment.environment_variables import EnvironmentVariables, reset_environment_variables


class GooConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):
        self.int1 = config_dict['int1']
        self.str2 = config_dict['str2']
        self.secrets = config_dict.get('secrets', {})  # { "secret_plain": "secret:test/app/fake-secret-plain","secret_pair": "secret:test/app/fake-secret-pair" }


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


@pytest.fixture()
def reset_env():
    reset_environment_variables()
    config_folder = os.path.join(pathlib.Path(__file__).parent.resolve(), 'config')
    os.environ['LOCAL_CONFIGURATION_FOLDER'] = config_folder


@pytest.fixture
def env_variables(reset_env):
    reset_environment_variables()
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'dev'
    os.environ['REGION'] = 'us-west-2'
    os.environ['SERVICE_NAME'] = 'test'

    return EnvironmentVariables()


@pytest.fixture
def app_configuration_provider(env_variables):
    return AppConfigConfigurationProvider(env_variables)


""" This test assumes the following resources exists:
    AppConfig app names 'test-app' with 'aws.dev.us-west-2' configuration profile, deployed to 'dev' environment.
    The configuration is described in tests/confug/aws.dev/us-west-2.json' file.
    In addition two secrets are stored on Secretes Manager:
    - Plain text secret: 'test/app/fake-secret-plain' = fake-secret-val
    - Key/Value secret: 'secret:test/app/fake-secret-pair': {
                'Username': 'fake-username',
                'Password': 'fake-password'
            }

    TODO (@limorl): Test can be imprived to deploy a newly created configuration and then deleted after test test
"""


@pytest.mark.integration
def test_init_and_get_configuration__success(
        app_configuration_provider,
        configuration,
        configuration_with_populated_secrets,
):

    app_configuration_provider.init_configuration()

    configuration: GooConfiguration = app_configuration_provider.get_configuration(GooConfiguration)

    # assert configuration is correct and secrets were populated
    assert configuration
    assert configuration.int1 == configuration_with_populated_secrets.int1
    assert configuration.str2 == configuration_with_populated_secrets.str2
    assert configuration.secrets['secret_plain'] == configuration_with_populated_secrets.secrets['secret_plain']
    assert configuration.secrets['secret_pair']['Username'] == configuration_with_populated_secrets.secrets['secret_pair']['Username']
    assert configuration.secrets['secret_pair']['Password'] == configuration_with_populated_secrets.secrets['secret_pair']['Password']
