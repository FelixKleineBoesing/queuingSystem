import unittest

from src.api.api import get_app
from tests.capacity_arguments import InboundArguments


class CapacityEndpointTester(unittest.TestCase):

    app = get_app()
    client = app.app.test_client()

class InboundTester(CapacityEndpointTester, InboundArguments):

    def test_inbound_phone_get_number_agents_for_service_level(self):
        pass
