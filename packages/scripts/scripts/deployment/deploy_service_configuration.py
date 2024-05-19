
import argparse
import boto3
from botocore.exceptions import ClientError
from enum import Enum
import json
import logging
import os
import time
from typing import Any, Dict
from configuration.configuration import ConfigurationSection
from configuration.app_config_utils import APP_CONFIG_REGION, compose_app_name, compose_config_name, app_config_get_application_id, app_config_get_deployment_strategy_id, app_config_get_environment_id, app_config_get_profile_id, app_config_create_hosted_configuration_version

logger = logging.getLogger()

# This assumes this service deployment strategy was created using Terraform. For now it was created manually.
DEFAULT_SERVICE_DEPLOYMENT_STARTEGY = 'linear-step20'


class DeploymentError(Exception):
    pass


class DeploymentState(Enum):
    BAKING = 'BAKING'
    VALIDATING = 'VALIDATING'
    DEPLOYING = 'DEPLOYING'
    COMPLETE = 'COMPLETE'
    ROLLING_BACK = 'ROLLING_BACK'
    ROLLED_BACK = 'ROLLED_BACK'

# TODO (limorl): Add --version argument to be used as VersionLable when calling create_hosted_configuration_version.
# The label should indicate the package version


def deploy_service_configuration(service_name: str, platform: str, stage: str, region: str) -> None:
    """Deploy service configuration to AWS AppConfig"""
    config_folder = 'config'
    config_name = compose_config_name(platform, stage, region)

    config_file = os.path.join(os.getcwd(), 'services', service_name, config_folder, f'{config_name}.json')

    if not os.path.exists(config_file):
        logger.warning(f'No configuration file found under {config_folder} folder for service {service_name}')
        return

    options = {}
    options['region_name'] = APP_CONFIG_REGION
    appconfig = boto3.client('appconfig', **options)

    app_name = compose_app_name(service_name)
    app_id = app_config_get_application_id(appconfig, app_name, True)
    env_id = app_config_get_environment_id(appconfig, app_id, stage, True)
    service_deployment_strategy_id = app_config_get_deployment_strategy_id(appconfig, DEFAULT_SERVICE_DEPLOYMENT_STARTEGY)

    try:
        with open(config_file, 'r') as file:
            logger.debug(f'Loading configuration file: {config_file}')
            config_json: Dict[str, ConfigurationSection] = json.load(file)

            config_profile_id = app_config_get_profile_id(appconfig, app_id, config_name, True)
            version_number = app_config_create_hosted_configuration_version(appconfig, app_id, config_profile_id, config_json)

            logger.info(f'Starting configuration deployment for app: {app_name}, config name: {config_name}, app id: {app_id}, profile: {config_profile_id}, version: {version_number}')

            deployment = appconfig.start_deployment(
                ApplicationId=app_id,
                ConfigurationProfileId=config_profile_id,
                ConfigurationVersion=str(version_number),
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


def _wait_until_deployment_completes(appconfig: Any, deployment: Dict[str, Any]) -> Dict[str, Any]:
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
    parser.add_argument('--service-name', type=str, required=True, help='The name of the service package, for example: greeting')
    parser.add_argument('--platform', type=str, required=False, default='AWS', help='The platform to deploy to, currently only AWS is supported')
    parser.add_argument('--stage', type=str, required=True, help='Stage in [prod|dev|staging]')
    parser.add_argument('--region', type=str, required=True, help='Region e.g., us-east-1')
    return parser


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    deploy_service_configuration(args.service_name, args.platform, args.stage, args.region)


if __name__ == "__main__":
    main()
