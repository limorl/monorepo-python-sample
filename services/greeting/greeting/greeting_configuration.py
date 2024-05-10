from configuration.configuration import Configuration, ConfigurationDict


class GreetingConfiguration(Configuration):

    def __init__(self, config_dict: ConfigurationDict):
        self.num_of_exclamations: int = config_dict.get('num_of_exclamations')
