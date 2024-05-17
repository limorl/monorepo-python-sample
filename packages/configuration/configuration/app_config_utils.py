
import json
import logging
from typing import Any, Callable, Dict, NewType

logger = logging.getLogger()

DEFAULT_ENVIRONMENT_NAME = 'prod'
DEFAULT_DEPLOYMENT_STARTEGY_NAME = 'service-deployment-strategy'  # This assumes this service deployment strategy was created using Terraform. For now it was created manually.

Deployment = NewType('Deployment', Dict)


def compose_config_name(platform: str, stage: str, region: str) -> str:
    return f'{platform.lower()}.{stage}.{region}'


def compose_app_name(service_name: str, stage: str, region: str) -> str:
    return f'{service_name}-{stage}-{region}'


def app_config_get_application_id(appconfig: Any, app_name: str, create_if_not_exists: bool = True) -> str:
    return _get_or_create_id(
        app_name,
        lambda next_token: appconfig.list_applications(NextToken=next_token) if next_token else appconfig.list_applications(),
        create_if_not_exists and (lambda: appconfig.create_application(Name=app_name))
    )


def app_config_get_environment_id(appconfig: Any, app_id: str, env_name: str, create_if_not_exists: bool = True) -> str:
    return _get_or_create_id(
        env_name,
        lambda next_token: appconfig.list_environments(ApplicationId=app_id, NextToken=next_token) if next_token else appconfig.list_environments(ApplicationId=app_id),
        create_if_not_exists and (lambda: appconfig.create_environment(ApplicationId=app_id, Name=env_name))
    )


def app_config_get_deployment_strategy_id(appconfig: Any, strategy_name: str = DEFAULT_DEPLOYMENT_STARTEGY_NAME) -> str:
    id = _get_id_by_name(
        strategy_name,
        lambda next_token: appconfig.list_deployment_strategies(NextToken=next_token) if next_token else appconfig.list_deployment_strategies()
    )

    if id:
        return id

    raise KeyError(f'Deployment strategy with name ${strategy_name} does not exist')


def app_config_get_profile_id(appconfig: Any, app_id: str, config_name: str, create_if_not_exists: bool = True) -> str:
    return _get_or_create_id(
        config_name,
        lambda next_token: appconfig.list_configuration_profiles(ApplicationId=app_id, NextToken=next_token) if next_token else appconfig.list_configuration_profiles(ApplicationId=app_id),
        create_if_not_exists and (lambda: appconfig.create_configuration_profile(ApplicationId=app_id, Name=config_name, LocationUri='hosted'))
    )


def app_config_data_get_latest_configuration(appconfigdata: Any, app_id: str, env_id: str, config_profile_id: str) -> Dict[str, Any]:
        
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
    configuration: Dict[str, Any] = json.loads(configuration_json)

    return configuration


def _get_or_create_id(name: str, list_func: Callable[[str], Dict], create_func: Callable[[], Dict] = None) -> str:
    id = _get_id_by_name(name, list_func)

    return id or (create_func and create_func().get('Id'))


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
