import os
from src import DEFAULT_VARIABLES


class ConfigManager:
    """
    The config manager accesses environment variables and default variables and can therefore be used in
    local development mode as well as in dockerized production
    """
    variables = {}

    def get_value(self, key: str):
        if key in ConfigManager.variables:
            return ConfigManager.variables[key]
        elif key in os.environ:
            return os.environ[key]
        elif key in DEFAULT_VARIABLES:
            return DEFAULT_VARIABLES[key]
        else:
            raise KeyError("Key not present!")

    def overwride_value(self, key: str, value):
        self.variables[key] = value
