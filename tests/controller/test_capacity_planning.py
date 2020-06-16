import unittest

from src.controller.capacity_planning_inbound_phone import InboundPhoneController
from src.controller.capacity_planning_inbound_chat import InboundChatController


class CapacityPlanningParameters(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.interval = [15 * 60, 10 * 60]
        cls.volume = [50, 40]
        cls.aht = [180, 170]
        cls.service_level = [0.9, 0.85]
        cls.service_time = [10, 15]
        cls.size_room = [100, 120]
        cls.patience = [180, 190]
        cls.retrial = [0.15, 0.25]
        cls.number_agents = [14, 15]
        cls.asa = [50, 60]
        cls.max_sessions = [5, 9]
        cls.share_sequential_work = [0.15, 0.22]


class CapacityPlanningInboundPhoneTester(CapacityPlanningParameters):

    controller = InboundPhoneController()

    def test_get_number_agents_for_service_level_list(self):
        number_agents = self.controller.get_number_agents_for_service_level(interval=self.interval,
                                                                            volume=self.volume,
                                                                            aht=self.aht,
                                                                            service_level=self.service_level,
                                                                            service_time=self.service_time)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 15)
        self.assertEqual(number_agents[1], 16)

        number_agents = self.controller.get_number_agents_for_service_level(interval=self.interval,
                                                                            volume=self.volume,
                                                                            aht=self.aht,
                                                                            service_level=self.service_level,
                                                                            service_time=self.service_time,
                                                                            size_room=self.size_room,
                                                                            patience=self.patience,
                                                                            retrial=self.retrial)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 14)
        self.assertEqual(number_agents[1], 15)

    def test_get_volume_for_service_level(self):
        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time)
        self.assertTrue(isinstance(volume, list))
        self.assertEqual(volume[0], 68.578125)
        self.assertEqual(volume[1], 51.49356617647059)

        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time,
                                                              size_room=self.size_room,
                                                              patience=self.patience,
                                                              retrial=self.retrial)

        self.assertTrue(isinstance(volume, list))
        self.assertEqual(volume[0], 100.40624999999999)
        self.assertEqual(volume[1], 71.6773897058823)

    def test_get_number_agents_for_average_waiting_time(self):
        number_agents = self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                                   volume=self.volume,
                                                                                   aht=self.aht,
                                                                                   asa=self.asa)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 58)
        self.assertEqual(number_agents[1], 11)

        number_agents = self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                                   volume=self.volume,
                                                                                   aht=self.aht,
                                                                                   asa=self.asa,
                                                                                   size_room=self.size_room,
                                                                                   patience=self.patience,
                                                                                   retrial=self.retrial)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 8)
        self.assertEqual(number_agents[1], 8)

    def test_get_volume_for_average_waiting_time(self):
        volumes = self.controller.get_volume_for_average_waiting_time(interval=self.interval,
                                                                      number_agents=self.number_agents,
                                                                      aht=self.aht,
                                                                      asa=self.asa)
        self.assertTrue(isinstance(volumes, list))
        self.assertEqual(volumes[0], 70.0)
        self.assertEqual(volumes[1], 52.94117647058823)

        volumes = self.controller.get_volume_for_average_waiting_time(interval=self.interval,
                                                                      number_agents=self.number_agents,
                                                                      aht=self.aht,
                                                                      asa=self.asa,
                                                                      size_room=self.size_room,
                                                                      patience=self.patience,
                                                                      retrial=self.retrial)

        self.assertTrue(isinstance(volumes, list))
        self.assertEqual(volumes[0], 95.40234374999999)
        self.assertEqual(volumes[1], 76.88878676470583)


class CapacityPlanningInboundChat(CapacityPlanningParameters):

    controller = InboundChatController()

    def test_get_number_agents_for_service_level(self):
        number_agents = \
            self.controller.get_number_agents_for_service_level(interval=self.interval,
                                                                volume=self.volume,
                                                                aht=self.aht,
                                                                service_level=self.service_level,
                                                                service_time=self.service_time,
                                                                max_sessions=self.max_sessions,
                                                                share_sequential_work=self.share_sequential_work)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 4)
        self.assertEqual(number_agents[1], 1)

        number_agents = \
            self.controller.get_number_agents_for_service_level(interval=self.interval,
                                                                volume=self.volume,
                                                                aht=self.aht,
                                                                service_level=self.service_level,
                                                                service_time=self.service_time,
                                                                max_sessions=self.max_sessions,
                                                                share_sequential_work=self.share_sequential_work,
                                                                size_room=self.size_room,
                                                                patience=self.patience,
                                                                retrial=self.retrial)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 3)
        self.assertEqual(number_agents[1], 1)

    def test_get_volume_for_service_level(self):
        # TODO this execution is slow as fuck
        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time,
                                                              max_sessions=self.max_sessions,
                                                              share_sequential_work=self.share_sequential_work)
        self.assertTrue(isinstance(volume, list))
        self.assertEqual(volume[0], 73.5)
        self.assertEqual(volume[1], 52.94117647058823)

        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time,
                                                              max_sessions=self.max_sessions,
                                                              share_sequential_work=self.share_sequential_work,
                                                              size_room=self.size_room,
                                                              patience=self.patience,
                                                              retrial=self.retrial)

        self.assertTrue(isinstance(volume, list))
        self.assertEqual(volume[0], 70)
        self.assertEqual(volume[1], 52.94117647058823)

    def test_get_number_agents_for_average_waiting_time(self):
        number_agents = \
            self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                       volume=self.volume,
                                                                       aht=self.aht,
                                                                       asa=self.asa,
                                                                       max_sessions=self.max_sessions,
                                                                       share_sequential_work=self.share_sequential_work)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 10)
        self.assertEqual(number_agents[1], 7)

        number_agents = \
            self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                       volume=self.volume,
                                                                       aht=self.aht,
                                                                       asa=self.asa,
                                                                       max_sessions=self.max_sessions,
                                                                       share_sequential_work=self.share_sequential_work,
                                                                       size_room=self.size_room,
                                                                       patience=self.patience,
                                                                       retrial=self.retrial)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 3)
        self.assertEqual(number_agents[1], 3)

    def test_get_volume_for_average_waiting_time(self):
        volumes = \
            self.controller.get_volume_for_average_waiting_time(interval=self.interval,
                                                                number_agents=self.number_agents,
                                                                aht=self.aht,
                                                                asa=self.asa,
                                                                max_sessions=self.max_sessions,
                                                                share_sequential_work=self.share_sequential_work)
        self.assertTrue(isinstance(volumes, list))
        self.assertEqual(volumes[0], 70.0)
        self.assertEqual(volumes[1], 90.66111845128668)

        volumes = \
            self.controller.get_volume_for_average_waiting_time(interval=self.interval,
                                                                number_agents=self.number_agents,
                                                                aht=self.aht,
                                                                asa=self.asa,
                                                                max_sessions=self.max_sessions,
                                                                share_sequential_work=self.share_sequential_work,
                                                                size_room=self.size_room,
                                                                patience=self.patience,
                                                                retrial=self.retrial)

        self.assertTrue(isinstance(volumes, list))
        self.assertEqual(volumes[0], 252.05468749999991)
        self.assertEqual(volumes[1], 576.6865808823521)