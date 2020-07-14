import unittest

from src.api.api import get_app, run_app


class ApiTester(unittest.TestCase):

    def test_get_app(self):
        app = get_app()

    def test_run_app(self):
        self.skipTest("Run in other process, request something and assert if available")
        run_app(get_app())

    def test_all_endpoints(self):
        app = get_app()
        rules = [rule.rule for rule in app.app.url_map.iter_rules()]

        self.assertIn("/capacity/outbound/phone/number-agents", rules)
        self.assertIn("/capacity/outbound/phone/volume", rules)
        self.assertIn("/capacity/inbound/phone/number-agents-for-average-waiting-time", rules)
        self.assertIn("/capacity/inbound/phone/number-agents-for-service-level", rules)
        self.assertIn("/capacity/inbound/phone/volume-for-average-waiting-time", rules)
        self.assertIn("/capacity/inbound/phone/volume-for-service-level", rules)
        self.assertIn("/capacity/inbound/chat/number-agents-for-average-waiting-time", rules)
        self.assertIn("/capacity/inbound/chat/number-agents-for-service-level", rules)
        self.assertIn("/capacity/inbound/chat/volume-for-average-waiting-time", rules)
        self.assertIn("/capacity/inbound/chat/volume-for-service-level", rules)
        self.assertIn("/capacity/backoffice/number-agents", rules)
        self.assertIn("/capacity/backoffice/volume", rules)
        self.assertIn("/openapi.json", rules)
        self.assertIn("/openapi.yaml", rules)
        self.assertIn("/ui/", rules)
        self.assertIn("/static/<path:filename>", rules)
        self.assertIn("/ui/<path:filename>", rules)


class ApiClient(unittest.TestCase):

    app = get_app()
    client = app.app.test_client()