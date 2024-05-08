from configuration.app_configuration_provider import IAppConfigurationProvider


class AppConfigAppConfigurationProvider(IAppConfigurationProvider):
    """TODO: Implement
    Configuration Provider based on AWS App Config.
    When deploying services, the configuration files under the service's /config folders are deployed"""
    def __init__(self):
        super().init()
        self.config = None

    def init_configuration(self):
        pass

    def get_config(self, key: str) -> str:
        return self.config.get(key, '')
