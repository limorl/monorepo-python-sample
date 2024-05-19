import json
import pytest
from unittest.mock import patch, Mock
from configuration.ssm_utils import is_secret, ssm_get_secret_value, _parse_secret
from botocore.exceptions import ClientError


@pytest.fixture
def mock_ssm_client():
    with patch('boto3.client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture(params=[['ssm:/fake/secret/name', True], ['not-a-secret', False], ['', False], [5, False]])
def is_secret_pair(request):
    return request.param

@pytest.fixture(params=[['/test/app/fake-secret-plain', 'fake-secret-val'], ['/test/app/fake-secret-pair', '{"Username": "fake-user", "Password": "fake-password"}']])
def secret_and_populated_secret(request):
    return request.param

def test_is_secret(is_secret_pair):
    assert is_secret(is_secret_pair[0]) == is_secret_pair[1]
    

def test_get_secret_success_string(mock_ssm_client, secret_and_populated_secret):
    secret_name = secret_and_populated_secret[0]
    expected_secret_val = _parse_secret(secret_and_populated_secret[1])

    mock_ssm_client.get_secret_value.return_value = {'SecretString': secret_and_populated_secret[1]}

    response = ssm_get_secret_value(mock_ssm_client, f'ssm:{secret_name}')

    mock_ssm_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
    _assert_equal_secret_values(response, expected_secret_val)


def test_get_secret_success_binary(mock_ssm_client, secret_and_populated_secret):
    secret_name = secret_and_populated_secret[0]
    expected_secret_val =_parse_secret(secret_and_populated_secret[1])

    mock_ssm_client.get_secret_value.return_value = {'SecretBinary': secret_and_populated_secret[1].encode('utf-8')}

    response = ssm_get_secret_value(mock_ssm_client, f'ssm:{secret_name}')

    mock_ssm_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
    _assert_equal_secret_values(response, expected_secret_val)


def test_get_secret_failure_non_existing_secret(mock_ssm_client):
    secret_name = 'fake-secret-non-existing-secret'

    mock_ssm_client.get_secret_value.side_effect = ClientError({"Error": {"Code": "ResourceNotFoundException"}}, "get_secret_value")

    with pytest.raises(ClientError):
        ssm_get_secret_value(mock_ssm_client, secret_name)


def test_get_secret_failure_secret_value_is_none(mock_ssm_client):
    secret_name = '/test/app/fake-secret'

    mock_ssm_client.get_secret_value.return_value = {}  # Both SecretString and SecretBinary are None

    with pytest.raises(ValueError):
        ssm_get_secret_value(mock_ssm_client, secret_name)

def _assert_equal_secret_values(secret_val, expected_secret_val):
    if not isinstance(secret_val, dict):
        assert secret_val == expected_secret_val
    else:
        assert json.dumps(secret_val) == json.dumps(expected_secret_val)
