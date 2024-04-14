from configuration.app.configuration_provider import IConfigurationProvider

class RemoteConfigurationProvider(IConfigurationProvider):
    """TODO: Implement
    AppConfigurationProvider consumes configuration from AWS App Config.
    As part of the deployment, the configuration files under /config are deployes per service and initialized here"""
    def __init__(self):
        super().init()
        self.config = None

    def init_configuration(self):
        pass


    def get_config(self, key: str) -> str:
        return self.config.get(key, '')
