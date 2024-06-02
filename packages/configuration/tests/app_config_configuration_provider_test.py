import os
import pytest
from botocore.exceptions import ClientError
from unittest.mock import Mock, patch
from configuration.app_config_configuration_provider import AppConfigConfigurationProvider
from configuration.configuration_provider import ConfigurationSection
from configuration.configuration import Configuration
from environment.service_environment import ServiceEnvironment, clear_service_environment, restore_local_dev_service_environment


class FooConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):
        self.int1 = config_dict['int1']
        self.str2 = config_dict['str2']
        self.section10 = config_dict.get('section10', {})
        self.secrets10 = config_dict.get('secrets10', {})


@pytest.fixture
def set_env():
    clear_service_environment()
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-west-2'
    os.environ['SERVICE_NAME'] = 'hello'

    yield ServiceEnvironment()
    restore_local_dev_service_environment()


@pytest.fixture
def mock_get_secret_value_responses():
    return [
        {'ARN': 'test-arn', 'SecretString': 'populated-fake-secret-1'},
        {'ARN': 'test-arn', 'SecretString': 'populated-fake-secret-2'}
    ]


@pytest.fixture
def app_configuration_provider(set_env):
    with patch('boto3.client') as mock_boto_client:
        mock_appconfig = Mock()
        mock_appconfigdata = Mock()
        mock_secretsmanager = Mock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_appconfig if service == 'appconfig' else (mock_appconfigdata if service == 'appconfigdata' else mock_secretsmanager)
        configuration_provider = AppConfigConfigurationProvider(service_env=set_env)
        return configuration_provider, mock_appconfig, mock_appconfigdata, mock_secretsmanager


def test_init_and_get_configuration_success(
        app_configuration_provider,
        mock_configuration_dict,
        mock_configuration_with_secrets_dict,
        mock_list_applications_response,
        mock_list_environments_response,
        mock_list_configuration_profiles_response,
        mock_start_configuration_session_response,
        mock_get_latest_configuration_response,
        mock_get_secret_value_responses
):

    config_provider, mock_appconfig, mock_appconfigdata, mock_secretsmanager = app_configuration_provider

    mock_appconfig.list_applications.return_value = mock_list_applications_response
    mock_appconfig.list_environments.return_value = mock_list_environments_response
    mock_appconfig.list_configuration_profiles.return_value = mock_list_configuration_profiles_response
    mock_appconfig.get_configuration.return_value = mock_configuration_dict

    mock_appconfigdata.start_configuration_session.return_value = mock_start_configuration_session_response
    mock_appconfigdata.get_latest_configuration.return_value = mock_get_latest_configuration_response

    mock_secretsmanager.get_secret_value.side_effect = mock_get_secret_value_responses

    config_provider.init_configuration()

    mock_appconfig.list_applications.assert_called_once()
    mock_appconfig.list_environments.assert_called_once()
    mock_appconfig.list_configuration_profiles.assert_called_once()

    mock_appconfigdata.start_configuration_session.assert_called_once()
    mock_appconfigdata.get_latest_configuration.assert_called_once()

    assert config_provider._app_name == 'hello-service'
    assert config_provider._config_name == 'aws.prod.us-west-2'

    foo_configuration: FooConfiguration = config_provider.get_configuration(FooConfiguration)
    expected_foo_configuration_dict = mock_configuration_with_secrets_dict['FooConfiguration']

    # assert configuration is correct and secrets were populated
    assert foo_configuration
    assert foo_configuration.int1 == expected_foo_configuration_dict['int1']
    assert foo_configuration.str2 == expected_foo_configuration_dict['str2']
    assert foo_configuration.section10['int10'] == expected_foo_configuration_dict['section10']['int10']
    assert foo_configuration.section10['str10'] == expected_foo_configuration_dict['section10']['str10']
    assert foo_configuration.secrets10['secret11'] == expected_foo_configuration_dict['secrets10']['secret11']
    assert foo_configuration.secrets10['secret12'] == expected_foo_configuration_dict['secrets10']['secret12']


def test_get_configuration_not_initialized_error(app_configuration_provider):
    config_provider, _, _, _ = app_configuration_provider

    with pytest.raises(RuntimeError):
        config_provider.get_configuration(FooConfiguration)


def test_init_configuration_app_config_data_error(
        app_configuration_provider,
        mock_configuration_dict,
        mock_list_applications_response,
        mock_list_environments_response,
        mock_list_configuration_profiles_response
):
    config_provider, mock_appconfig, mock_appconfigdata, _ = app_configuration_provider

    mock_appconfig.list_applications.return_value = mock_list_applications_response
    mock_appconfig.list_environments.return_value = mock_list_environments_response
    mock_appconfig.list_configuration_profiles.return_value = mock_list_configuration_profiles_response
    mock_appconfig.get_configuration.return_value = mock_configuration_dict

    mock_appconfigdata.start_configuration_session.side_effect = ClientError({"Error": {"Code": "InternalServerException"}}, "start_configuration_session")

    with pytest.raises(ClientError):
        config_provider.init_configuration()
