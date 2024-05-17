import pytest
from unittest.mock import patch, Mock
from configuration.ssm_utils import *
from botocore.exceptions import ClientError

@pytest.fixture
def mock_ssm_client():
    with patch('boto3.client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client


def test_get_secret_success_string(mock_ssm_client):
    secret_name = 'test/app/fake-secret'
    expected_secret_val = 'fake-secret-sdbhe-dmlf-127nd'
    
    mock_ssm_client.get_secret_value.return_value = {'SecretString': expected_secret_val}

    response = ssm_get_secret_value(mock_ssm_client, f'ssm:{secret_name}')

    mock_ssm_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
    assert response == expected_secret_val


def test_get_secret_success_binary(mock_ssm_client):
    secret_name = 'test/app/fake-secret'
    expected_secret_val = 'fake-secret-sdbhe-dmlf-127nd'
    
    mock_ssm_client.get_secret_value.return_value = {'SecretBinary': expected_secret_val.encode('utf-8')}

    response = ssm_get_secret_value(mock_ssm_client, f'ssm:{secret_name}')

    mock_ssm_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
    assert response == expected_secret_val


def test_get_secret_failure_non_existing_secret(mock_ssm_client):
    secret_name = 'fake-secret-non-existing-secret'

    mock_ssm_client.get_secret_value.side_effect = ClientError({"Error": {"Code": "ResourceNotFoundException"}}, "get_secret_value")

    with pytest.raises(ClientError) as err:
        ssm_get_secret_value(mock_ssm_client, secret_name)


def test_get_secret_failure_secret_value_is_none(mock_ssm_client):
    secret_name = 'test/app/fake-secret'

    mock_ssm_client.get_secret_value.return_value = {}  # Both SecretString and SecretBinary are None

    
    with pytest.raises(ValueError):
        ssm_get_secret_value(mock_ssm_client, secret_name)
