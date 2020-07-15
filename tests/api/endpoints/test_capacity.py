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
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [14, 15])

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/phone/number-agents-for-service-level", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [14, 14])

    def test_inbound_phone_get_volume_for_service_level(self):
        body = {"interval": self.interval,
                "number_agents": self.number_agents,
                "aht": self.aht,
                "service_level": self.service_level,
                "service_time": self.service_time}
        response = self.client.post("/capacity/inbound/phone/volume-for-service-level", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        volumes = [47.57812500000002, 39.457720588235254]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/phone/volume-for-service-level", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["status_code"], 200)
        volumes = [50.203125000000014, 42.4770220588235]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

    def test_inbound_phone_get_number_agents_for_average_waiting_time(self):
        body = {"interval": self.interval,
                "volume": self.volume,
                "aht": self.aht,
                "asa": self.asa}
        response = self.client.post("/capacity/inbound/phone/number-agents-for-average-waiting-time", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [12, 13])

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/phone/number-agents-for-average-waiting-time", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [8, 8])

    def test_inbound_phone_get_volume_for_average_waiting_time(self):
        body = {"interval": self.interval,
                "number_agents": self.number_agents,
                "aht": self.aht,
                "asa": self.asa}
        response = self.client.post("/capacity/inbound/phone/volume-for-average-waiting-time", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        volumes = [70.0, 52.94117647058823]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/phone/volume-for-average-waiting-time", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["status_code"], 200)
        volumes = [95.40234374999999, 76.88878676470583]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

    def test_inbound_chat_get_number_agents_for_service_level(self):
        body = {"interval": self.interval,
                "volume": self.volume,
                "aht": self.aht,
                "service_level": self.service_level,
                "service_time": self.service_time,
                "max_sessions": self.max_sessions,
                "share_sequential_work": self.share_sequential_work}
        response = self.client.post("/capacity/inbound/chat/number-agents-for-service-level", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [5, 2])

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/number-agents-for-service-level", json=body).json
        if response["status_code"] == 400:
            print(response["message"])
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [2, 3])

    def test_inbound_chat_get_volume_for_service_level(self):
        body = {"interval": self.interval,
                "volume": self.volume,
                "aht": self.aht,
                "service_level": self.service_level,
                "service_time": self.service_time,
                "max_sessions": self.max_sessions,
                "share_sequential_work": self.share_sequential_work}
        response = self.client.post("/capacity/inbound/chat/volume-for-service-level", json=body).json
        self.assertEqual(response["status_code"], 200)
        volumes = [47.57812500000002, 39.457720588235254]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/volume-for-service-level", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["status_code"], 200)
        volumes = [50.203125000000014, 42.4770220588235]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

    def test_inbound_chat_get_number_agents_for_average_waiting_time(self):
        body = {"interval": self.interval,
                "volume": self.volume,
                "aht": self.aht,
                "asa": self.asa,
                "max_sessions": self.max_sessions,
                "share_sequential_work": self.share_sequential_work}
        response = self.client.post("/capacity/inbound/chat/number-agents-for-average-waiting-time", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [14, 15])

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/number-agents-for-average-waiting-time", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [14, 14])

    def test_inbound_chat_get_volume_for_average_waiting_time(self):
        body = {"interval": self.interval,
                "number_agents": self.number_agents,
                "aht": self.aht,
                "asa": self.asa,
                "max_sessions": self.max_sessions,
                "share_sequential_work": self.share_sequential_work}
        response = self.client.post("/capacity/inbound/chat/number-agents-for-average-waiting-time", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [14, 15])

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/number-agents-for-average-waiting-time", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [14, 14])