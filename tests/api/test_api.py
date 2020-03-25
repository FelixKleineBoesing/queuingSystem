import unittest

from src.api.api import get_app, run_app


class ApiTester(unittest.TestCase):

    def test_get_app(self):
        self.skipTest("Not implemented yet!")
        app = get_app()

    def test_run_app(self):
        self.skipTest("Not implemented yet!")
        run_app(get_app())