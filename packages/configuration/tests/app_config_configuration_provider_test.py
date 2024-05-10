""" import json
import os
from unittest.mock import patch, MagicMock
import pytest
from configuration.configuration_provider import Configuration
from configuration.app_config_configuration_provider import AppConfigConfigurationProvider
from environment.environment_variables import EnvironmentVariables, reset_environment_variables
from typing import Dict, Any

@pytest.fixture
def aws_prod_env():
    # reset_environment_variables()
    os.environ['PLATFORM'] = 'aws'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'region'
    os.environ['SERVICE_NAME'] = 'service'

    yield EnvironmentVariables()

@pytest.fixture
def app_config_configuration_provider(aws_prod_env):
    with patch('configuration.app_config_configuration_provider.boto3') as mock_boto3:
        mock_app_config = mock_boto3.client.return_value
        mock_ssm = mock_boto3.client.return_value

        mock_app_config.list_applications.side_effect = [
            {'Items': [{'Name': 'App1'}, {'Name': 'App2'}], 'NextToken': 'token'},
            {'Items': [{'Name': 'App3'}, {'Name': 'service-prod-region', 'Id': 'app-id'}]},
        ]
        mock_app_config.list_configuration_profiles.side_effect = [
            {'Items': [{'Name': 'FooConfig'}], 'NextToken': 'token'},
            {'Items': [{'Name': 'BarConfig'}]},
        ]
        mock_app_config.get_configuration.side_effect = [
            {'Content': json.dumps({'size': 10, 'message': 'hi'}).encode()},
            {'Content': json.dumps({'url': 'url.com', 'arr': ['value1', 'value2'], 'queue': {'should_persist': False, 'token': 'SECRET'}}).encode()},
        ]
        mock_ssm.get_parameter.return_value = {'Parameter': {'Value': 'SECRET'}}
        yield AppConfigConfigurationProvider(aws_prod_env)

class FooConfig(Configuration):
    size: int
    message: str


class BarConfig(Configuration):
    url: str
    queue: Dict[str, Any]


@pytest.mark.asyncio
async def test_configuration_provider_init_configurations(app_config_configuration_provider):
    await app_config_configuration_provider.init_configuration()
    foo_config = app_config_configuration_provider.get_configuration(FooConfig)

    assert foo_config.size == 10
    assert foo_config.message == 'hi'

    bar_config = app_config_configuration_provider.get_configuration(BarConfig)
    assert bar_config.url == 'url.com'
    assert bar_config.arr == ['value1', 'value2']
    assert bar_config.queue.shouldPersist is False
    assert bar_config.queue.token == 'SECRET'
 """
