import unittest

from src.controller.capacity_planning.single_skill.inbound_phone import InboundPhoneController
from src.controller.capacity_planning.single_skill.inbound_chat import InboundChatController
from tests.capacity_arguments import InboundArguments


class CapacityPlanningInboundPhoneTester(unittest.TestCase, InboundArguments):

    controller = InboundPhoneController()

    def test_get_number_agents_for_service_level_list(self):
        number_agents = self.controller.get_number_agents_for_service_level(interval=self.interval,
                                                                            volume=self.volume,
                                                                            aht=self.aht,
                                                                            service_level=self.service_level,
                                                                            service_time=self.service_time)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 14)
        self.assertEqual(number_agents[1], 15)

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
        self.assertEqual(number_agents[1], 14)

    def test_get_volume_for_service_level(self):
        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time)
        self.assertTrue(isinstance(volume, list))
        self.assertEqual(volume[0], 47.57812500000002)
        self.assertEqual(volume[1], 39.457720588235254)

        volume = self.controller.get_volume_for_service_level(interval=self.interval,
                                                              number_agents=self.number_agents,
                                                              aht=self.aht,
                                                              service_level=self.service_level,
                                                              service_time=self.service_time,
                                                              size_room=self.size_room,
                                                              patience=self.patience,
                                                              retrial=self.retrial)

        self.assertTrue(isinstance(volume, list))
        self.assertEqual(volume[0], 50.203125000000014)
        self.assertEqual(volume[1], 42.4770220588235)

    def test_get_number_agents_for_average_waiting_time(self):
        number_agents = self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                                   volume=self.volume,
                                                                                   aht=self.aht,
                                                                                   asa=self.asa)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 12)
        self.assertEqual(number_agents[1], 13)

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


class CapacityPlanningInboundChat(unittest.TestCase, InboundArguments):

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
        self.assertEqual(number_agents[0], 5)
        self.assertEqual(number_agents[1], 2)

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
        self.assertEqual(number_agents[0], 2)
        self.assertEqual(number_agents[1], 3)

    def test_get_volume_for_service_level(self):
        # TODO this execution is slow as fuck
        import cProfile
        profile = cProfile.Profile()
        profile.enable()
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
        self.assertEqual(volume[0], 70.0)
        self.assertEqual(volume[1], 52.94117647058823)
        profile.disable()
        profile.dump_stats("cProfile.cprof")
        profile.print_stats()

    def test_get_number_agents_for_average_waiting_time(self):
        number_agents = \
            self.controller.get_number_agents_for_average_waiting_time(interval=self.interval,
                                                                       volume=self.volume,
                                                                       aht=self.aht,
                                                                       asa=self.asa,
                                                                       max_sessions=self.max_sessions,
                                                                       share_sequential_work=self.share_sequential_work)
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(number_agents[0], 18)
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
        self.assertEqual(number_agents[0], 1)
        self.assertEqual(number_agents[1], 1)

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
        self.assertEqual(volumes[1], 91.38686236213228)

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
