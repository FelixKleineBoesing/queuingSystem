from tests.api.test_api import ApiClient
from tests.capacity_arguments import InboundArguments


class InboundTester(ApiClient, InboundArguments):

    def test_inbound_phone_get_number_agents_for_service_level(self):
        body = {"interval": self.interval,
                "volume": self.volume,
                "aht": self.aht,
                "service_level": self.service_level,
                "service_time": self.service_time}
        response = self.client.post("/capacity/inbound/phone/number-agents-for-service-level", json=body).json

        