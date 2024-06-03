import json
import logging
import os
import pathlib
import time
from enum import Enum
from typing import Any, Callable

import boto3
from botocore.exceptions import ClientError
from environment.service_environment import Platform, Stage, get_primary_region

from .configuration import ConfigurationSection

logger = logging.getLogger()

# This assumes this service deployment strategy was created using Terraform. For now it was created manually.
SERVICE_DEFAULT_DEPLOYMENT_STARTEGY = 'ServiceDefault.Linear'
SERVICE_DEV_DEPLOYMENT_STRATEGY = 'Test.Linear.AllatOnce'


class DeploymentError(Exception):
    pass


class DeploymentState(Enum):
    BAKING = 'BAKING'
    VALIDATING = 'VALIDATING'
    DEPLOYING = 'DEPLOYING'
    COMPLETE = 'COMPLETE'
    ROLLING_BACK = 'ROLLING_BACK'
    ROLLED_BACK = 'ROLLED_BACK'


def get_app_name(service_name: str) -> str:
    return f'{service_name}-service'


def get_config_name(platform: Platform, stage: Stage, region: str) -> str:
    return f'{platform.value.lower()}.{stage.value}.{region}'


def app_config_get_application_id(appconfig: Any, app_name: str, create_if_not_exists: bool = False) -> str:
    return _get_or_create_id(
        app_name,
        (lambda next_token: appconfig.list_applications(NextToken=next_token)
         if next_token
         else appconfig.list_applications()),
        create_if_not_exists and (lambda: appconfig.create_application(Name=app_name))
    )


def app_config_get_environment_id(appconfig: Any,
                                  app_id: str, env_name: str, create_if_not_exists: bool = False) -> str:
    return _get_or_create_id(
        env_name,
        (lambda next_token: appconfig.list_environments(ApplicationId=app_id, NextToken=next_token)
         if next_token
         else appconfig.list_environments(ApplicationId=app_id)),
        create_if_not_exists and (lambda: appconfig.create_environment(ApplicationId=app_id, Name=env_name))
    )


def app_config_get_deployment_strategy_id(appconfig: Any, strategy_name: str) -> str:
    strategy_id = _get_id_by_name(
        strategy_name,
        (lambda next_token: appconfig.list_deployment_strategies(NextToken=next_token)
         if next_token
         else appconfig.list_deployment_strategies())
    )

    if strategy_id:
        return strategy_id

    raise KeyError(f'Deployment strategy with name ${strategy_name} does not exist')


def app_config_get_profile_id(appconfig: Any, app_id: str, config_name: str, create_if_not_exists: bool = False) -> str:
    return _get_or_create_id(
        config_name,
        (lambda next_token: appconfig.list_configuration_profiles(ApplicationId=app_id, NextToken=next_token)
         if next_token
         else appconfig.list_configuration_profiles(ApplicationId=app_id)),
        create_if_not_exists and (
            lambda: appconfig.create_configuration_profile(ApplicationId=app_id, Name=config_name, LocationUri='hosted')
        )
    )


def app_config_create_hosted_configuration_version(appconfig: Any, app_id: str, config_profile_id: str,
                                                   configuration: dict[str, ConfigurationSection]) -> int:
    config_bytes = json.dumps(configuration).encode('utf-8')

    version = appconfig.create_hosted_configuration_version(
        ApplicationId=app_id,
        ConfigurationProfileId=config_profile_id,
        Content=config_bytes,
        ContentType='application/json'
    )

    return version.get('VersionNumber')


def app_config_data_get_latest_configuration(appconfigdata: Any, app_id: str, env_id: str,
                                             config_profile_id: str) -> dict[str, Any]:
    initial_configuration_token = appconfigdata.start_configuration_session(
        ApplicationIdentifier=app_id,
        EnvironmentIdentifier=env_id,
        ConfigurationProfileIdentifier=config_profile_id
    ).get('InitialConfigurationToken')

    # For now we assume we're getting the latest configuration is one round
    response = appconfigdata.get_latest_configuration(
        ConfigurationToken=initial_configuration_token
    )

    configuration_json = response['Configuration'].read()
    configuration: dict[str, Any] = json.loads(configuration_json)

    return configuration


def app_config_deploy_service_configuration(service_name: str, platform: Platform, stage: Stage, region: str,
                                            deployment_strategy_name: str = SERVICE_DEFAULT_DEPLOYMENT_STARTEGY,
                                            config_dir: str | None = None) -> None:
    config_name = get_config_name(platform, stage, region)

    monorepo_root = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
    config_dir = config_dir or os.path.join(monorepo_root, 'services', 'service_name', 'config')
    config_file = os.path.join(config_dir, f'{config_name}.json')

    if not os.path.exists(config_file):
        logger.warning(f'Configuration file for service {service_name} does not exist: {config_file}')
        return

    options = {}
    options['region_name'] = get_primary_region(stage)
    appconfig = boto3.client('appconfig', **options)

    app_name = get_app_name(service_name)
    app_id = app_config_get_application_id(appconfig, app_name, create_if_not_exists=True)
    env_id = app_config_get_environment_id(appconfig, app_id, stage.value, create_if_not_exists=True)
    service_deployment_strategy_id = app_config_get_deployment_strategy_id(appconfig, deployment_strategy_name)

    try:
        with open(config_file) as file:
            logger.debug(f'Loading configuration file: {config_file}')
            config_json: dict[str, ConfigurationSection] = json.load(file)

            config_profile_id = app_config_get_profile_id(appconfig, app_id, config_name, create_if_not_exists=True)
            version_number = app_config_create_hosted_configuration_version(
                appconfig, app_id, config_profile_id, config_json
            )

            logger.info(f'Starting configuration deployment for app: {app_name}, config name: {config_name}, app id: {app_id}, profile: {config_profile_id}, version: {version_number}')  # noqa: E501

            deployment = appconfig.start_deployment(
                ApplicationId=app_id,
                ConfigurationProfileId=config_profile_id,
                ConfigurationVersion=str(version_number),
                EnvironmentId=env_id,
                DeploymentStrategyId=service_deployment_strategy_id
            )

            deployment = _wait_until_deployment_completes(appconfig, deployment)

    except json.JSONDecodeError:
        logger.exception(f'Failed to decode JSON from configuration file: {config_file}')
    except ClientError as err:
        error_code = err["Error"]["Code"]
        logger.exception(f'Failed to deploy configuration for service: {service_name}. Error Code: {error_code}')
    except DeploymentError:
        logger.exception(f'Failed to deploy configuration for service: {service_name}.')


def _wait_until_deployment_completes(appconfig: Any, deployment: dict[str, Any]) -> dict[str, Any]:
    deployment_state = DeploymentState(deployment.get('State'))

    while deployment_state != DeploymentState.COMPLETE:
        if deployment_state in (DeploymentState.ROLLED_BACK, DeploymentState.ROLLING_BACK):
            event_log = deployment.get('EventLog')
            event_log_str = event_log and (entry.get('Description').join('\n') for entry in event_log)
            raise DeploymentError(f'Configuration deployment failed. Details:\n ${event_log_str}')

        time.sleep(1)
        deployment = appconfig.get_deployment(
            ApplicationId=deployment.get('ApplicationId'),
            DeploymentNumber=deployment.get('DeploymentNumber'),
            EnvironmentId=deployment.get('EnvironmentId')
        )

    return deployment


def _get_or_create_id(name: str, list_func: Callable[[str], dict],
                      create_func: Callable[[], dict] | None = None) -> str:
    item_id = _get_id_by_name(name, list_func)

    return item_id or (create_func and create_func().get('Id'))


def _get_id_by_name(name: str, list_func: Callable[[str], dict]) -> str:
    next_token: str = None
    first_time: bool = True

    while first_time or next_token:
        first_time = False
        items_dict = list_func(next_token)
        matches = items_dict.get('Items') and list(filter(lambda x: x.get('Name') == name, items_dict.get('Items')))
        if matches and len(matches) > 0:
            return matches[0].get('Id')

        next_token = items_dict.get('NextToken')

    return None
