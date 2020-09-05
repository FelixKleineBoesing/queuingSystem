import unittest

from src.misc.config_manager import ConfigManager


class ConfigManagerTester(unittest.TestCase):

    def test_construction(self):
        config_manager = ConfigManager()
