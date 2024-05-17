import os
import pytest
from unittest.mock import Mock, patch
from configuration.app_config_configuration_provider import AppConfigConfigurationProvider
from configuration.configuration_provider import ConfigurationDict
from configuration.configuration import Configuration
from environment.environment_variables import EnvironmentVariables, reset_environment_variables
from configuration.app_config_utils import *
from configuration.ssm_utils import *


class FooConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationDict):
        self.int1 = config_dict['int1']
        self.str2 = config_dict['str2']
        self.section10 = config_dict.get('section10', {})
        self.secrets10 = config_dict.get('secrets10', {})


@pytest.fixture
def env_variables():
    reset_environment_variables()
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-west-2'
    os.environ['SERVICE_NAME']= 'hello'

    return EnvironmentVariables()


@pytest.fixture
def app_name(env_variables):
    return compose_app_name(env_variables.service_name, env_variables.stage.value, env_variables.region)


@pytest.fixture
def config_name(env_variables):
    return compose_config_name(env_variables.platform.value, env_variables.stage.value, env_variables.region)


@pytest.fixture
def mock_get_secret_value_responses():
   return [
       {'ARN': 'test-arn', 'SecretString': 'populated-fake-secret-11'},
       {'ARN': 'test-arn', 'SecretString': 'populated-fake-secret-12'}
   ]


@pytest.fixture
def app_configuration_provider(env_variables):
    with patch('boto3.client') as mock_boto_client:
        mock_appconfig = Mock()
        mock_appconfigdata = Mock()
        mock_ssm = Mock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_appconfig if service == 'appconfig' else (mock_appconfigdata if service == 'appconfigdata' else mock_ssm)
        configuration_provider = AppConfigConfigurationProvider(env_vars=env_variables)
        return configuration_provider, mock_appconfig, mock_appconfigdata, mock_ssm


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
    
    config_provider, mock_appconfig, mock_appconfigdata, mock_ssm = app_configuration_provider

    mock_appconfig.list_applications.return_value = mock_list_applications_response
    mock_appconfig.list_environments.return_value = mock_list_environments_response
    mock_appconfig.list_configuration_profiles.return_value = mock_list_configuration_profiles_response
    mock_appconfig.get_configuration.return_value = mock_configuration_dict

    mock_appconfigdata.start_configuration_session.return_value = mock_start_configuration_session_response
    mock_appconfigdata.get_latest_configuration.return_value = mock_get_latest_configuration_response

    mock_ssm.get_secret_value.side_effect = mock_get_secret_value_responses

    config_provider.init_configuration()

    mock_appconfig.list_applications.assert_called_once()
    mock_appconfig.list_environments.assert_called_once()
    mock_appconfig.list_configuration_profiles.assert_called_once()

    mock_appconfigdata.start_configuration_session.assert_called_once()
    mock_appconfigdata.get_latest_configuration.assert_called_once()
    
    assert config_provider._app_name == 'hello-prod-us-west-2'
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

