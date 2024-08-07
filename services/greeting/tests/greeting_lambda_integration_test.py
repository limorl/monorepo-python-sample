
# This test assumes a Greeting service is pre-deployed by Github Workflows / Manually
import boto3
import json
import os
import pathlib
from greeting.app import AppConfiguration
import pytest

from configuration.local_configuration_provider import LocalConfigurationProvider
from environment.service_environment import ServiceEnvironment, Stage, get_primary_region, clear_service_environment, restore_local_dev_service_environment
from greeting.greeting import GreetingConfiguration


@pytest.fixture
def integration_test_env():
    return Stage(os.environ['INTEGRATION_TEST_ENV'])


@pytest.fixture
def lambda_client(integration_test_env):
    region = get_primary_region(integration_test_env)
    options: dict = {'region_name': region}

    return boto3.client('lambda', **options)


@pytest.fixture
def service_env(integration_test_env):
    clear_service_environment()
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = integration_test_env.value
    os.environ['REGION'] = get_primary_region(integration_test_env)
    os.environ['SERVICE_NAME'] = 'greeting'

    config_folder = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), 'config')
    os.environ['LOCAL_CONFIGURATION_FOLDER'] = config_folder

    yield ServiceEnvironment()
    restore_local_dev_service_environment()


@pytest.fixture
def configuration_provider(service_env):
    configuration_provider = LocalConfigurationProvider(service_env)
    configuration_provider.init_configuration()
    return configuration_provider


@pytest.mark.integration
def test_greeting_lambda_hello(lambda_client, configuration_provider):
    app_config = configuration_provider.get_configuration(AppConfiguration)
    greeting_config = configuration_provider.get_configuration(GreetingConfiguration)
    expected_greeting = f'Hello {"!" * greeting_config.num_of_exclamations}'
    expected_payload_body = f'<{app_config.html_heading}>{expected_greeting}</{app_config.html_heading}>'

    response = lambda_client.invoke(
        FunctionName='greeting',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload='{"headers": {}, "path": "/hello", "httpMethod": "GET"}'
    )

    assert response['StatusCode'] == 200
    payload_body = json.loads(response['Payload'].read())['body']
    assert payload_body == expected_payload_body
