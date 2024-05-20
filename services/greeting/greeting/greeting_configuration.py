from configuration.configuration import Configuration, ConfigurationSection


class GreetingConfiguration(Configuration):
    def __init__(self, config_dict: ConfigurationSection):