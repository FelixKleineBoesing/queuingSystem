import unittest

from src.controller.capacity_planning_inbound_phone import InboundPhoneController


class CapacityPlanningInboundPhoneTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.controller = InboundPhoneController()
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

    def test_get_number_agents_for_service_level_list(self):
        number_agents = self.controller.get_number_agents_for_service_level(interval=self.interval,
                                                                            volume=self.volume,
                                                                            aht=self.aht,
                                                                            service_level=self.service_level,
                                                                            service_time=self.service_time)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 15)
        self.assertEqual(number_agents[0], 16)

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
        self.assertEqual(number_agents[0], 15)

    def test_get_volume_for_service_level(self):
        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time)
        print(volume)

        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time,
                                                              size_room=self.size_room,
                                                              patience=self.patience,
                                                              retrial=self.retrial)

        print(volume)

    def test_get_number_agents_for_average_waiting_time(self):
        number_agents = self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                                   volume=self.volume,
                                                                                   aht=self.aht,
                                                                                   asa=self.asa)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 58)
        self.assertEqual(number_agents[0], 58)

        number_agents = self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                                   volume=self.volume,
                                                                                   aht=self.aht,
                                                                                   asa=self.asa,
                                                                                   size_room=self.size_room,
                                                                                   patience=self.patience,
                                                                                   retrial=self.retrial)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 8)
        self.assertEqual(number_agents[0], 8)

    def test_get_volume_for_average_waiting_time(self):
        volume = self.controller.get_volume_for_average_waiting_time(interval=self.interval,
                                                                     number_agents=self.number_agents,
                                                                     aht=self.aht,
                                                                     asa=self.asa,
                                                                     service_level=self.service_level,
                                                                     service_time=self.service_time)
        print(volume)

        volume = self.controller.get_volume_for_average_waiting_time(interval=self.interval,
                                                                     number_agents=self.number_agents,
                                                                     aht=self.aht,
                                                                     asa=self.asa,
                                                                     service_level=self.service_level,
                                                                     service_time=self.service_time,
                                                                     size_room=self.size_room,
                                                                     patience=self.patience,
                                                                     retrial=self.retrial)

        print(volume)