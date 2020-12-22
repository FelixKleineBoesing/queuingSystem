import unittest

from src.controller.capacity_planning.single_skill.outbound_phone import OutboundPhoneController
from tests.capacity_arguments import OutboundArguments


class CapacityPlanningOutboundTester(OutboundArguments, unittest.TestCase):

    outbound = OutboundPhoneController()

    def test_get_number_agents(self):
        number_agents = self.outbound.get_number_agents(interval=self.interval, volume=self.volume,
                                                        dialing_time=self.dialing_time,
                                                        aht_correct=self.aht_correct, aht_wrong=self.aht_wrong,
                                                        netto_contact_rate=self.netto_contact_rate,
                                                        right_person_contact_rate=self.right_person_contact_rate)
        self.assertTrue(isinstance(number_agents, list))
        self.assertTrue(number_agents[0], 1.6800000000000004)
        self.assertTrue(number_agents[1], 10.2)

    def test_get_volume(self):
        volume = self.outbound.get_volume(interval=self.interval, number_agents=self.number_agents,
                                          dialing_time=self.dialing_time, aht_correct=self.aht_correct,
                                          aht_wrong=self.aht_wrong,
                                          netto_contact_rate=self.netto_contact_rate,
                                          right_person_contact_rate=self.right_person_contact_rate)
        self.assertTrue(isinstance(volume, list))
        print(volume)
        self.assertEqual(volume[0], 19.999999999999996)
        self.assertEqual(volume[1], 7.843137254901961)
