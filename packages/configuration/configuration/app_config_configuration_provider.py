from configuration.configuration_provider import IConfigurationProvider


class AppConfigAppConfigurationProvider(IConfigurationProvider):
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
