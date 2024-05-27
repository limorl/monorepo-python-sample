import json
import pytest
from unittest.mock import patch, Mock
from configuration.secret import parse_secret_value
from configuration.secrets_manager_utils import secrets_manager_get_secret_value
from botocore.exceptions import ClientError


@pytest.fixture
def mock_secretsmanager():
    with patch('boto3.client') as mock:
        mock_client = Mock()
        mock.return_value = mock_client
        yield mock_client


@pytest.fixture(params=[['test/app/fake-secret-plain', 'fake-secret-val'], ['test/app/fake-secret-pair', '{"Username": "fake-user", "Password": "fake-password"}']])
def secret_and_populated_secret(request):
    return request.param


def test_get_secret_success_string(mock_secretsmanager, secret_and_populated_secret):
    secret_name = secret_and_populated_secret[0]
    expected_secret_val = parse_secret_value(secret_and_populated_secret[1])

    mock_secretsmanager.get_secret_value.return_value = {'SecretString': secret_and_populated_secret[1]}

    response = secrets_manager_get_secret_value(mock_secretsmanager, f'secret:{secret_name}')

    mock_secretsmanager.get_secret_value.assert_called_once_with(SecretId=secret_name)
    _assert_equal_secret_values(response, expected_secret_val)


def test_get_secret_success_binary(mock_secretsmanager, secret_and_populated_secret):
    secret_name = secret_and_populated_secret[0]
    expected_secret_val = parse_secret_value(secret_and_populated_secret[1])

    mock_secretsmanager.get_secret_value.return_value = {'SecretBinary': secret_and_populated_secret[1].encode('utf-8')}

    response = secrets_manager_get_secret_value(mock_secretsmanager, f'secret:{secret_name}')

    mock_secretsmanager.get_secret_value.assert_called_once_with(SecretId=secret_name)
    _assert_equal_secret_values(response, expected_secret_val)


def test_get_secret_failure_non_existing_secret(mock_secretsmanager):
    secret_name = 'fake-secret-non-existing-secret'

    mock_secretsmanager.get_secret_value.side_effect = ClientError({"Error": {"Code": "ResourceNotFoundException"}}, "get_secret_value")

    with pytest.raises(ClientError):
        secrets_manager_get_secret_value(mock_secretsmanager, secret_name)


def test_get_secret_failure_secret_value_is_none(mock_secretsmanager):
    secret_name = '/test/app/fake-secret'

    mock_secretsmanager.get_secret_value.return_value = {}  # Both SecretString and SecretBinary are None

    with pytest.raises(ValueError):
        secrets_manager_get_secret_value(mock_secretsmanager, secret_name)


def _assert_equal_secret_values(secret_val, expected_secret_val):
    if not isinstance(secret_val, dict):
        assert secret_val == expected_secret_val
    else:
        assert json.dumps(secret_val) == json.dumps(expected_secret_val)
