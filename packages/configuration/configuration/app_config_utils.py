
import json
import logging
from typing import Any, Callable, Dict
from .configuration import ConfigurationSection

logger = logging.getLogger()


def compose_config_name(platform: str, stage: str, region: str) -> str:
    return f'{platform.lower()}.{stage}.{region}'


def compose_app_name(service_name: str, stage: str, region: str) -> str:
    return f'{service_name}-{stage}-{region}'


def app_config_get_application_id(appconfig: Any, app_name: str, create_if_not_exists: bool = False) -> str:
    return _get_or_create_id(
        app_name,
        lambda next_token: appconfig.list_applications(NextToken=next_token) if next_token else appconfig.list_applications(),
        create_if_not_exists and (lambda: appconfig.create_application(Name=app_name))
    )


def app_config_get_environment_id(appconfig: Any, app_id: str, env_name: str, create_if_not_exists: bool = False) -> str:
    return _get_or_create_id(
        env_name,
        lambda next_token: appconfig.list_environments(ApplicationId=app_id, NextToken=next_token) if next_token else appconfig.list_environments(ApplicationId=app_id),
        create_if_not_exists and (lambda: appconfig.create_environment(ApplicationId=app_id, Name=env_name))
    )


def app_config_get_deployment_strategy_id(appconfig: Any, strategy_name: str) -> str:
    id = _get_id_by_name(
        strategy_name,
        lambda next_token: appconfig.list_deployment_strategies(NextToken=next_token) if next_token else appconfig.list_deployment_strategies()
    )

    if id:
        return id

    raise KeyError(f'Deployment strategy with name ${strategy_name} does not exist')


def app_config_get_profile_id(appconfig: Any, app_id: str, config_name: str, create_if_not_exists: bool = False) -> str:
    return _get_or_create_id(
        config_name,
        lambda next_token: appconfig.list_configuration_profiles(ApplicationId=app_id, NextToken=next_token) if next_token else appconfig.list_configuration_profiles(ApplicationId=app_id),
        create_if_not_exists and (lambda: appconfig.create_configuration_profile(ApplicationId=app_id, Name=config_name, LocationUri='hosted'))
    )


def app_config_create_hosted_configuration_version(appconfig: Any, app_id: str, config_profile_id: str, configuration: Dict[str, ConfigurationSection]) -> int:
    config_bytes = json.dumps(configuration).encode('utf-8')

    version = appconfig.create_hosted_configuration_version(
        ApplicationId=app_id,
        ConfigurationProfileId=config_profile_id,
        Content=config_bytes,
        ContentType='application/json'
    )

    return version.get('VersionNumber')


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
