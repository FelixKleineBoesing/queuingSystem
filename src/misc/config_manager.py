import os
import dotenv
from src import DEFAULT_VARIABLES


class ConfigManager:
    """
    The config manager accesses environment variables and default variables and can therefore be used in
    local development mode as well as in dockerized production
    """
    variables = {}

    def __init__(self, env_file: str = ".env"):
        """

        :param env_file:
        """
        if os.path.isfile(env_file):
            dotenv.load_dotenv(env_file)
        else:
            raise FileNotFoundError("env file is not found")

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
