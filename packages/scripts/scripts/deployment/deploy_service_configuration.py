
import argparse
import boto3
from botocore.exceptions import ClientError
from enum import Enum
import json
import logging
import os
import time
from typing import Any, Callable, Dict, NewType

logger = logging.getLogger()

DEFAULT_ENVIRONMENT_NAME = 'default'
SERVICE_DEPLOYMENT_STARTEGY_NAME = 'service-deployment'  # This assumes this service deployment strategy was created using Terraform. For now it was created manually.

Deployment = NewType('Deployment', Dict)


class DeploymentError(Exception):
    pass


class DeploymentState(Enum):
    BAKING = 'BAKING'
    VALIDATING = 'VALIDATING'
    DEPLOYING = 'DEPLOYING'
    COMPLETE = 'COMPLETE'
    ROLLING_BACK = 'ROLLING_BACK'
    ROLLED_BACK = 'ROLLED_BACK'


def deploy_service_configuration(service_name: str, stage: str, region: str) -> None:
    """Deploy service configuration to AWS AppConfig"""
    config_folder = 'config'
    config_name = f'aws.{stage}.{region}'
    config_file = os.path.join(os.getcwd(), 'services', service_name, config_folder, f'{config_name}.json')

    if not os.path.exists(config_file):
        logger.warn(f'No configuration file found under {config_folder} folder for service {service_name}')
        return

    options = {}
    options['region_name'] = region
    appconfig = boto3.client('appconfig', **options)

    app_name = f'{service_name}-{stage}-{region}'
    app_id = _get_or_create_app_config_application(appconfig, app_name)
    env_id = _get_or_create_app_config_environment(appconfig, app_id, DEFAULT_ENVIRONMENT_NAME)
    service_deployment_strategy_id = _get_deployment_strategy_id(appconfig, SERVICE_DEPLOYMENT_STARTEGY_NAME)

    try:
        with open(config_file, 'r') as file:
            logger.debug(f'Loading configuration file: {config_file}')
            config_json_str = json.dumps(json.load(file))
            config_bytes = config_json_str.encode('utf-8')

            config_profile_id = _get_or_create_app_config_profile(appconfig, app_id, config_name)
            hosted_configuration_version = appconfig.create_hosted_configuration_version(
                ApplicationId=app_id,
                ConfigurationProfileId=config_profile_id,
                Content=config_bytes,
                ContentType='application/json'
            )

            version_number = str(hosted_configuration_version.get('VersionNumber'))
            logger.info(f'Starting configuration deployment for app: {app_name}, config name: {config_name}, app id: {app_id}, profile: {config_profile_id}, version: {version_number}')

            deployment = appconfig.start_deployment(
                ApplicationId=app_id,
                ConfigurationProfileId=config_profile_id,
                ConfigurationVersion=version_number,
                EnvironmentId=env_id,
                DeploymentStrategyId=service_deployment_strategy_id
            )

            deployment = _wait_until_deployment_completes(appconfig, deployment)

    except json.JSONDecodeError:
        logger.error(f'Failed to decode JSON from configuration file: {config_file}')
    except ClientError as err:
        logger.error(f'Failed to deploy configuration for service: {service_name}. Error Code: {err["Error"]["Code"]} error: {err}')
    except DeploymentError as err:
        logger.error(f'Failed to deploy configuration for service: {service_name}. Error: {err}')


def _get_or_create_app_config_application(appconfig: Any, app_name: str) -> str:
   # list_func = lambda next_token: appconfig.list_applications(NextToken=next_token) if next_token else appconfig.list_applications()
   # create_func = lambda: appconfig.create_application(Name=app_name)

    return _get_or_create(app_name,
                          lambda next_token: appconfig.list_applications(NextToken=next_token) if next_token else appconfig.list_applications(),
                          lambda: appconfig.create_application(Name=app_name)
                        )


def _get_or_create_app_config_environment(appconfig: Any, app_id: str, env_name: str) -> str:
    list_func = lambda next_token: appconfig.list_environments(ApplicationId=app_id, NextToken=next_token) if next_token else appconfig.list_environments(ApplicationId=app_id)
    create_func = lambda: appconfig.create_environment(ApplicationId=app_id, Name=env_name)

    return _get_or_create(env_name, list_func, create_func)


def _get_deployment_strategy_id(appconfig: Any, strategy_name: str) -> str:
    list_func = lambda next_token: appconfig.list_deployment_strategies(NextToken=next_token) if next_token else appconfig.list_deployment_strategies()
    id = _get_id_by_name(strategy_name, list_func)
    
    if id:
        return id
    
    raise KeyError(f'Deployment strategy with name ${strategy_name} does not exist')


def _get_or_create_app_config_profile(appconfig: Any, app_id: str, config_name: str) -> str:
    list_func = lambda next_token: appconfig.list_configuration_profiles(ApplicationId=app_id, NextToken=next_token) if next_token else appconfig.list_configuration_profiles(ApplicationId=app_id)
    create_func = lambda: appconfig.create_configuration_profile(ApplicationId=app_id, Name=config_name, LocationUri='hosted')

    return _get_or_create(config_name, list_func, create_func)


def _get_or_create(name: str, list_func: Callable[[str], Dict], create_func: Callable[[], Dict]) -> str:
    return _get_id_by_name(name, list_func) or create_func().get('Id')


def _get_id_by_name(name: str, list_func: Callable[[str], Dict]) -> str:
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


def _wait_until_deployment_completes(appconfig: Any, deployment: Deployment) -> Deployment:
    deployment_state = DeploymentState(deployment.get('State'))

    while deployment_state != DeploymentState.COMPLETE:
        if deployment_state == DeploymentState.ROLLED_BACK or deployment_state == DeploymentState.ROLLING_BACK:
            event_log = deployment.get('EventLog') and map(lambda entry: entry.get('Description').join('\n'), deployment.get('EventLog'))
            raise DeploymentError(f'Configuration deployment failed. Details:\n ${event_log}')
        
        time.sleep(1)
        deployment = appconfig.get_deployment(
            ApplicationId=deployment.get('ApplicationId'),
            DeploymentNumber=deployment.get('DeploymentNumber'),
            EnvironmentId=deployment.get('EnvironmentId')
        )
    
    return deployment


def _create_arg_parser():
    parser = argparse.ArgumentParser(prog='deploy_service_configuration.py', description='Deploy service configuration to AWS AppConfig')
    parser.add_argument('--service-name', type = str, required = True, help = 'The name of the service package, for example: greeting')
    parser.add_argument('--stage', type = str, required = True, help = 'Stage in [prod|dev|staging]')
    parser.add_argument('--region', type = str, required = True, help = 'Region e.g., us-east-1')
    return parser


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    deploy_service_configuration(args.service_name, args.stage, args.region)


if __name__ == "__main__":
    main()