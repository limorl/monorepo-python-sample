import os
import pathlib
import pytest
from environment.environment_variables import EnvironmentVariables, Platform, Stage, reset_environment_variables


@pytest.fixture
def reset_env():
    reset_environment_variables()


@pytest.fixture
def test_data_dir():
    return os.path.join(pathlib.Path(__file__).parent.resolve(), '__data__')


@pytest.fixture
def default_local_config_folder():
    return os.path.join(os.getcwd(), 'config')


def test_init_environment_variables_dev_env(reset_env):
    os.environ['PLATFORM'] = 'local'
    os.environ['STAGE'] = 'dev'
    os.environ['CLOUD_ENDPOINT_OVERRIDE'] = 'http://localhost:4566'
    env = EnvironmentVariables()

    assert env.platform == Platform.LOCAL
    assert env.cloud_endpoint_override == 'http://localhost:4566'
    assert env.stage == Stage.DEV


def test_init_environment_variables_prod_env(reset_env, default_local_config_folder):
    os.environ['PLATFORM'] = 'AWS'
    os.environ['REGION'] = 'us-east-1'
    os.environ['STAGE'] = 'prod'
    os.environ['SERVICE_NAME'] = 'hello'
    env = EnvironmentVariables()

    assert env.platform == Platform.AWS
    assert env.region == 'us-east-1'
    assert env.service_name == 'hello'
    assert env.stage == Stage.PROD
    assert env.local_configuration_folder == default_local_config_folder


def test_init_environment_variables_empty_env_should_not_fail(reset_env, default_local_config_folder):
    env = EnvironmentVariables()

    assert env is not None
    assert env.platform is None
    assert env.stage is None
    assert env.region is None
    assert env.service_name is None
    assert env.cloud_endpoint_override is None
    assert env.local_configuration_folder == default_local_config_folder


def test_init_environment_variables_dev_dotenv_path(reset_env, test_data_dir, default_local_config_folder):
    dotnev_path = os.path.join(test_data_dir, '.dev.env')
    env = EnvironmentVariables(dotnev_path)

    assert env.platform == Platform.LOCAL
    assert env.cloud_endpoint_override == 'http://localhost:4566'
    assert env.service_name == 'hello'
    assert env.stage == Stage.DEV
    assert env.local_configuration_folder == default_local_config_folder


def test_init_environment_variables_prod_dotenv_path(reset_env, test_data_dir, default_local_config_folder):
    dotnev_path = os.path.join(test_data_dir, '.prod.env')
    env = EnvironmentVariables(dotnev_path)

    assert env.platform == Platform.AWS
    assert env.region == 'us-east-1'
    assert env.service_name == 'hello'
    assert env.stage == Stage.PROD
    assert env.local_configuration_folder == default_local_config_folder


def test_init_environment_variables_dotenv_empty(reset_env, test_data_dir, default_local_config_folder):
    dotnev_path = os.path.join(test_data_dir, '.empty.env')
    env = EnvironmentVariables(dotnev_path)

    assert env.platform is None
    assert env.region is None
    assert env.service_name is None
    assert env.cloud_endpoint_override is None
    assert env.local_configuration_folder == default_local_config_folder
    assert env.stage is None


def test_init_environment_variables_dotenv_with_config_folder(reset_env, test_data_dir, default_local_config_folder):
    dotnev_path = os.path.join(test_data_dir, '.local.config.folder.env')
    env = EnvironmentVariables(dotnev_path)

    assert env.local_configuration_folder == 'configfolder'


def test_init_environment_variables_dotenv_unknown_platform_should_throw(reset_env, test_data_dir):
    dotnev_path = os.path.join(test_data_dir, '.unknown.platform.env')
    with pytest.raises(ValueError) as exc_info:
        EnvironmentVariables(dotnev_path)

    assert "'foo' is not a valid Platform" in str(exc_info.value)


def test_init_environment_variables_dotenv_unknown_stage_should_throw(reset_env, test_data_dir):
    dotnev_path = os.path.join(test_data_dir, '.unknown.stage.env')

    with pytest.raises(ValueError) as exc_info:
        EnvironmentVariables(dotnev_path)

    assert "'goo' is not a valid Stage" in str(exc_info.value)


def test_get_configuration_aws_prod_missing_service_name_should_throw_value_error(reset_env):
    os.environ['PLATFORM'] = 'AWS'
    os.environ['STAGE'] = 'prod'
    os.environ['REGION'] = 'us-east-1'

    with pytest.raises(ValueError) as exc_info:
        EnvironmentVariables()

    assert "Missing service name" in str(exc_info.value)
