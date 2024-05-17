import pytest
from configuration.app_config_utils import compose_app_name, compose_config_name, app_config_get_application_id, app_config_get_environment_id, app_config_get_deployment_strategy_id, app_config_data_get_latest_configuration, app_config_get_profile_id, app_config_create_hosted_configuration_version


def test_compose_app_name():
    assert compose_app_name('my-service', 'dev', 'us-west-2') == 'my-service-dev-us-west-2'


def test_compose_config_name():
    assert compose_config_name('AWS', 'prod', 'us-east-1') == 'aws.prod.us-east-1'


# TODO (limorl): Add tests with NextToken and to handle when create_if_not_exists = False

def test_app_config_get_application_id_app_exists(mock_appconfig, mock_list_applications_response):
    mock_appconfig.list_applications.return_value = mock_list_applications_response

    app_id = app_config_get_application_id(mock_appconfig, mock_list_applications_response['Items'][0]['Name'])

    mock_appconfig.list_applications.assert_called_once()
    assert not mock_appconfig.create_application.called
    assert app_id == mock_list_applications_response['Items'][0]['Id']


def test_app_config_get_application_id_app_does_not_exist_create(mock_appconfig, mock_list_applications_response, mock_create_application_reponse):
    mock_list_applications_response['Items'] = []
    mock_appconfig.list_applications.return_value = mock_list_applications_response
    mock_appconfig.create_application.return_value = mock_create_application_reponse

    app_id = app_config_get_application_id(mock_appconfig, mock_create_application_reponse['Id'], True)

    mock_appconfig.list_applications.assert_called_once()
    mock_appconfig.create_application.assert_called_once()
    assert app_id == mock_create_application_reponse['Id']


def test_app_config_get_environment_id_env_exists(mock_appconfig, mock_list_environments_response):
    mock_appconfig.list_environments.return_value = mock_list_environments_response

    app_id = mock_list_environments_response['Items'][1]['ApplicationId']
    env_name = mock_list_environments_response['Items'][1]['Name']
    env_id = app_config_get_environment_id(mock_appconfig, app_id, env_name, True)

    mock_appconfig.list_environments.assert_called_once()
    assert not mock_appconfig.create_environments.called
    assert env_id == mock_list_environments_response['Items'][1]['Id']


def test_app_config_get_environment_id_env_exists_env_does_not_exist_create(mock_appconfig, mock_list_environments_response, mock_create_environment_reponse):
    mock_list_environments_response['Items'] = []
    mock_appconfig.list_environments.return_value = mock_list_environments_response
    mock_appconfig.create_environment.return_value = mock_create_environment_reponse

    app_id = mock_create_environment_reponse['Id']
    env_name = mock_create_environment_reponse['Name']
    env_id = app_config_get_environment_id(mock_appconfig, app_id, env_name, True)

    mock_appconfig.list_environments.assert_called_once()
    mock_appconfig.create_environment.assert_called_once()
    assert env_id == mock_create_environment_reponse['Id']


def test_pp_config_get_deployment_strategy_id_stratey_exists(mock_appconfig, mock_list_deployment_strategies_response):
    mock_appconfig.list_deployment_strategies.return_value = mock_list_deployment_strategies_response

    strategy_name = mock_list_deployment_strategies_response['Items'][0]['Name']
    strategy_id = app_config_get_deployment_strategy_id(mock_appconfig, strategy_name)

    mock_appconfig.list_deployment_strategies.assert_called_once()
    assert strategy_id == mock_list_deployment_strategies_response['Items'][0]['Id']


def test_app_config_get_deployment_strategy_id_does_not_exist_expected_error(mock_appconfig, mock_list_deployment_strategies_response):
    strategy_name = mock_list_deployment_strategies_response['Items'][0]['Name']
    mock_list_deployment_strategies_response['Items'] = []
    mock_appconfig.list_deployment_strategies.return_value = mock_list_deployment_strategies_response

    with pytest.raises(KeyError) as err:
        app_config_get_deployment_strategy_id(mock_appconfig, strategy_name)
        assert 'strategy with name' in err.message


def test_app_config_get_profile_id_profile_exists(mock_appconfig, mock_list_configuration_profiles_response):
    mock_appconfig.list_configuration_profiles.return_value = mock_list_configuration_profiles_response

    app_id = mock_list_configuration_profiles_response['Items'][0]['ApplicationId']
    profile_name = mock_list_configuration_profiles_response['Items'][0]['Name']
    profile_id = app_config_get_profile_id(mock_appconfig, app_id, profile_name, True)

    mock_appconfig.list_configuration_profiles.assert_called_once()
    assert not mock_appconfig.create_configuration_profile.called
    assert profile_id == mock_list_configuration_profiles_response['Items'][0]['Id']


def test_app_config_get_profile_id_profile_does_not_exist_create(mock_appconfig, mock_list_configuration_profiles_response, mock_create_configuration_profile_response):
    mock_list_configuration_profiles_response['Items'] = []
    mock_appconfig.list_configuration_profiles.return_value = mock_list_configuration_profiles_response
    mock_appconfig.create_configuration_profile.return_value = mock_create_configuration_profile_response

    app_id = mock_create_configuration_profile_response['ApplicationId']
    config_name = mock_create_configuration_profile_response['Name']
    profile_id = app_config_get_profile_id(mock_appconfig, app_id, config_name, True)

    mock_appconfig.list_configuration_profiles.assert_called_once()
    mock_appconfig.create_configuration_profile.assert_called_once()
    assert profile_id == mock_create_configuration_profile_response['Id']


def test_app_config_create_hosted_configuration_version_success(mock_appconfig, mock_configuration_dict, mock_create_hosted_configuration_version_response):
    mock_appconfig.create_hosted_configuration_version.return_value = mock_create_hosted_configuration_version_response

    app_id = mock_create_hosted_configuration_version_response['ApplicationId']
    profile_id = mock_create_hosted_configuration_version_response['ConfigurationProfileId']
    version_number = app_config_create_hosted_configuration_version(mock_appconfig, app_id, profile_id, mock_configuration_dict)

    assert version_number == mock_create_hosted_configuration_version_response['VersionNumber']


def test_app_config_data_get_latest_configuration_success(
    mock_appconfigdata,
    mock_configuration_dict,
    mock_start_configuration_session_response,
    mock_get_latest_configuration_response
):
    mock_appconfigdata.start_configuration_session.return_value = mock_start_configuration_session_response
    mock_appconfigdata.get_latest_configuration.return_value = mock_get_latest_configuration_response

    response = app_config_data_get_latest_configuration(mock_appconfigdata, 'app_id', 'env_id', 'profile_id')

    mock_appconfigdata.start_configuration_session.assert_called_once()
    mock_appconfigdata.get_latest_configuration.assert_called_once()

    assert response['FooConfiguration']
    assert response['FooConfiguration']['int1'] == mock_configuration_dict['FooConfiguration']['int1']
    assert response['FooConfiguration']['str2'] == mock_configuration_dict['FooConfiguration']['str2']
    assert response['FooConfiguration']['section10']['int10'] == mock_configuration_dict['FooConfiguration']['section10']['int10']
    assert response['FooConfiguration']['section10']['str10'] == mock_configuration_dict['FooConfiguration']['section10']['str10']
    assert response['FooConfiguration']['secrets10']['secret11'] == mock_configuration_dict['FooConfiguration']['secrets10']['secret11']
    assert response['FooConfiguration']['secrets10']['secret12'] == mock_configuration_dict['FooConfiguration']['secrets10']['secret12']
