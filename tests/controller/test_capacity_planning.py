import unittest

from src.controller.capacity_planning_inbound_phone import InboundPhoneController


class CapacityPlanningInboundPhoneTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.controller = InboundPhoneController()

    def test_get_number_agents_for_service_level(self):
        interval = 15 * 60
        volume = 50
        aht = 180
        service_level = 0.9
        service_time = 10
        number_agents = self.controller.get_number_agents_for_service_level(interval=interval, volume=volume, aht=aht,
                                                                            service_level=service_level,
                                                                            service_time=service_time)
        print(number_agents)

        size_room = 100
        patience = 180
        retrial = 0.15
        number_agents = self.controller.get_number_agents_for_service_level(interval=interval, volume=volume,
                                                                            aht=aht, service_level=service_level,
                                                                            service_time=service_time,
                                                                            size_room=size_room, patience=patience,
                                                                            retrial=retrial)
        print(number_agents)

    def test_get_volume_for_service_level(self):
        interval = 15 * 60
        number_agents = 14
        aht = 180
        service_level = 0.9
        service_time = 10
        lambda_ = self.controller.get_volume_for_service_level(interval=interval, number_agents=number_agents,
                                                               aht=aht,
                                                               service_level=service_level,
                                                               service_time=service_time)
        print(lambda_)

        size_room = 100
        patience = 180
        retrial = 0.15
        lambda_ = self.controller.get_volume_for_service_level(interval=interval, number_agents=number_agents,
                                                               aht=aht, service_level=service_level,
                                                               service_time=service_time,
                                                               size_room=size_room, patience=patience,
                                                               retrial=retrial)

        print(lambda_)

    def test_get_number_agents_for_average_waiting_time(self):
        pass

    def test_get_volume_for_average_waiting_time(self):
        pass