from tests.api.test_api import ApiClient
from tests.capacity_arguments import InboundArguments, BackOfficeArguments, OutboundArguments


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
                "number_agents": self.number_agents,
                "aht": self.aht,
                "service_level": self.service_level,
                "service_time": self.service_time,
                "max_sessions": self.max_sessions,
                "share_sequential_work": self.share_sequential_work}
        response = self.client.post("/capacity/inbound/chat/volume-for-service-level", json=body).json
        self.assertEqual(response["status_code"], 200)
        volumes = [73.5, 52.94117647058823]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/volume-for-service-level", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["status_code"], 200)
        volumes = [70.0, 52.94117647058823]
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
        self.assertEqual(response["result"], [18, 7])

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/number-agents-for-average-waiting-time", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [1, 1])

    def test_inbound_chat_get_volume_for_average_waiting_time(self):
        body = {"interval": self.interval,
                "number_agents": self.number_agents,
                "aht": self.aht,
                "asa": self.asa,
                "max_sessions": self.max_sessions,
                "share_sequential_work": self.share_sequential_work}
        response = self.client.post("/capacity/inbound/chat/volume-for-average-waiting-time", json=body).json
        volumes = [70.0, 91.38686236213228]
        self.assertEqual(response["status_code"], 200)
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)

        body["size_room"] = self.size_room
        body["patience"] = self.patience
        body["retrial"] = self.retrial

        response = self.client.post("/capacity/inbound/chat/volume-for-average-waiting-time", json=body).json
        self.assertEqual(response["status_code"], 200)
        volumes = [252.05468749999991, 576.6865808823521]
        for vol_hat, vol in zip(response["result"], volumes):
            self.assertAlmostEqual(vol, vol_hat, places=6)


class OutboundTester(ApiClient, OutboundArguments):

    def test_outbound_phone_get_number_agents(self):
        body = {"interval": self.interval,
                "volume": self.volume,
                "dialing_time": self.dialing_time,
                "netto_contact_rate": self.netto_contact_rate,
                "right_person_contact_rate": self.right_person_contact_rate,
                "aht_correct": self.aht_correct,
                "aht_wrong": self.aht_wrong}
        response = self.client.post("/capacity/outbound/phone/number-agents", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [1.6800000000000004, 10.2])

    def test_outbound_phone_get_volume(self):
        body = {"interval": self.interval,
                "number_agents": self.number_agents,
                "dialing_time": self.dialing_time,
                "netto_contact_rate": self.netto_contact_rate,
                "right_person_contact_rate": self.right_person_contact_rate,
                "aht_correct": self.aht_correct,
                "aht_wrong": self.aht_wrong}
        response = self.client.post("/capacity/outbound/phone/volume", json=body).json
        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["result"], [19.999999999999996, 7.843137254901961])


class BackOfficeTester(ApiClient, BackOfficeArguments):

    def test_backoffice_get_number_agents(self):
        body = {"interval": self.interval,
                "volume": self.lambdas,
                "backlog_sum": self.backlog_sums,
                "occupancy": self.occupancy,
                "aht": self.ahts,
                "backlog_within": self.backlog_within}
        response = self.client.post("/capacity/backoffice/number-agents", json=body).json
        self.assertEqual(response["status_code"], 200)
        for na_hat, na in zip(response["result"], self.number_agents):
            for item_hat, item in zip(na_hat, na):
                self.assertAlmostEqual(item_hat, item, places=6)

        self.assertEqual(response["result"], self.number_agents)

    def test_backoffice_get_volume(self):
        body = {"interval": self.interval,
                "number_agents": self.number_agents,
                "occupancy": self.occupancy,
                "aht": self.ahts,
                "backlog_within": self.backlog_within}
        response = self.client.post("/capacity/backoffice/volume", json=body).json
        self.assertEqual(response["status_code"], 200)
        for v_hat, v in zip(response["result"], self.lambdas_with_backlog):
            for item_hat, item in zip(v_hat, v):
                self.assertAlmostEqual(item_hat, item, places=6)
