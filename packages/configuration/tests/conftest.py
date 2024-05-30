import json
import pytest
from unittest.mock import Mock, patch
from botocore.response import StreamingBody
from io import StringIO

""" Shared Fixtures """


@pytest.fixture
def mock_boto_client():
    with patch('boto3.client') as mock:
        yield mock


@pytest.fixture
def mock_appconfig(mock_boto_client):
    mock_appconfig = Mock()
    mock_boto_client.return_value = mock_appconfig
    return mock_appconfig


@pytest.fixture
def mock_appconfigdata(mock_boto_client):
    mock_appconfigdata = Mock()
    mock_boto_client.return_value = mock_appconfigdata
    return mock_appconfigdata


@pytest.fixture
def mock_configuration_dict():
    config_dict = {
        "FooConfiguration": {
            "int1": 1,
            "str2": "2",
            "section10": {
                "int10": 10,
                "str10": "10"
            },
            "secrets10": {
                "secret11": "secret:test/app/fake-secret-1",
                "secret12": "secret:test/app/fake-secret-2"
            }
        }
    }
    return config_dict


@pytest.fixture
def mock_configuration_with_secrets_dict():
    config_dict = {
        "FooConfiguration": {
            "int1": 1,
            "str2": "2",
            "section10": {
                "int10": 10,
                "str10": "10"
            },
            "secrets10": {
                "secret11": "populated-fake-secret-1",
                "secret12": "populated-fake-secret-2"
            }
        }
    }
    return config_dict


@pytest.fixture
def mock_list_applications_response():
    return {
        'Items': [
            {'Id': 'app-123', 'Name': 'test-service-prod-us-west-2'},
            {'Id': 'app-456', 'Name': 'test-service-dev-us-east-1'}
        ]
    }


@pytest.fixture
def mock_create_application_reponse():
    return {
        'Id': 'id-789',
        'Name': 'name-789',
        'Description': 'decription-789'
    }


@pytest.fixture
def mock_list_environments_response():
    return {
        'Items': [
            {'ApplicationId': 'app-123', 'Id': 'env-123', 'Name': 'name-123', 'State': 'READY_FOR_DEPLOYMENT'},
            {'ApplicationId': 'app-456', 'Id': 'env-456', 'Name': 'name-456', 'State': 'READY_FOR_DEPLOYMENT'},
        ]
    }


@pytest.fixture
def mock_create_environment_reponse():
    return {
        'ApplicationId': 'app-789',
        'Id': 'id-789',
        'Name': 'env-789',
        'Description': 'description-789',
        'State': 'READY_FOR_DEPLOYMENT',
        'Monitors': []
    }


@pytest.fixture
def mock_list_deployment_strategies_response():
    return {
        'Items': [
            {
                'Id': 'id-123',
                'Name': 'strategy-123',
            },
            {
                'Id': 'id-456',
                'Name': 'strategy-456',
            },
        ]
    }


@pytest.fixture
def mock_list_configuration_profiles_response():
    return {
        'Items': [
            {'ApplicationId': 'app-123', 'Id': 'profile123', 'Name': 'name-123'},
            {'ApplicationId': 'app-456', 'Id': 'profile456', 'Name': 'name-456'}
        ]
    }


@pytest.fixture
def mock_create_configuration_profile_response():
    return {
        'ApplicationId': 'app-789',
        'Id': 'id-789',
        'Name': 'profile-789',
    }


@pytest.fixture
def mock_create_hosted_configuration_version_response():
    return {
        'ApplicationId': 'app-789',
        'ConfigurationProfileId': 'id-789',
        'VersionNumber': 3,
    }


@pytest.fixture
def mock_start_configuration_session_response():
    return {
        'InitialConfigurationToken': 'initial-token'
    }


@pytest.fixture
def mock_get_latest_configuration_response(mock_configuration_dict):
    config_json_str = json.dumps(mock_configuration_dict)
    return {
        # 'NextPollConfigurationToken': 'next-config-token',
        'NextPollIntervalInSeconds': 123,
        'ContentType': 'application/json',
        'Configuration': StreamingBody(StringIO(config_json_str), len(config_json_str)),
        'VersionLabel': 'test-label'
    }
