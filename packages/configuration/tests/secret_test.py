import pytest
from configuration.secret import is_secret, try_get_secret_name, parse_secret_value



@pytest.fixture(params=[['secret:fake/secret/name', True], ['not-a-secret', False], ['', False], [5, False]])
def is_secret_with_expected_result(request):
    return request.param


@pytest.fixture(params=[['secret:fake/secret/name', 'fake/secret/name'], ['not-a-secret', None], ['', None]])
def get_secret_name_with_expected_result(request):
    return request.param

@pytest.fixture(params=[['fake-secret-val', 'fake-secret-val'], ['{"Username": "fake-user", "Password": "fake-password"}', {"Username": "fake-user", "Password": "fake-password"}], ['', '']])
def parse_secret_with_expected_result(request):
    return request.param


def test_is_secret(is_secret_with_expected_result):
    assert is_secret(is_secret_with_expected_result[0]) == is_secret_with_expected_result[1]


def test_try_get_secret_name(get_secret_name_with_expected_result):
    assert try_get_secret_name(get_secret_name_with_expected_result[0]) == get_secret_name_with_expected_result[1]


def test_parse_secret_value(parse_secret_with_expected_result):
     assert parse_secret_value(parse_secret_with_expected_result[0]) == parse_secret_with_expected_result[1]


