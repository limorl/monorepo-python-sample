from configuration.configuration_provider import Configuration, ConfigurationDict


class AppConfiguration(Configuration):

    def __init__(self, config_dict: ConfigurationDict):
        self.numOfExclamations: int = config_dict.get('numOfExclamations')