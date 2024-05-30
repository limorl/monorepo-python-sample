from configuration.configuration import Configuration, ConfigurationSection


class GreetingConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):
        self.num_of_exclamations: int = config_dict.get('num_of_exclamations')
