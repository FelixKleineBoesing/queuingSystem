import unittest

from src.controller.capacity_planning.outbound_phone import OutboundPhoneController


class CapacityPlanningParameters(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.interval = [30 * 60, 10 * 60]
        cls.volume = [20, 40]
        cls.dialing_time = [5, 10]
        cls.netto_contract_rate = [0.9, 0.85]
        cls.right_person_contact_rate = [0.8, 0.75]
        cls.aht_correct = [200, 170]
        cls.aht_wrong = [15, 170]
        cls.number_agents = [1.68, 2]


class CapacityPlanningOutboundTester(CapacityPlanningParameters):

    outbound = OutboundPhoneController()

    def test_get_number_agents(self):
        number_agents = self.outbound.get_number_agents(interval=self.interval, volume=self.volume,
                                                        dialing_time=self.dialing_time,
                                                        aht_correct=self.aht_correct, aht_wrong=self.aht_wrong,
                                                        netto_contact_rate=self.netto_contract_rate,
                                                        right_person_contact_rate=self.right_person_contact_rate)
        self.assertTrue(isinstance(number_agents, list))
        self.assertTrue(number_agents[0], 1.6800000000000004)
        self.assertTrue(number_agents[1], 10.2)

    def test_get_volume(self):
        volume = self.outbound.get_volume(interval=self.interval, number_agents=self.number_agents,
                                          dialing_time=self.dialing_time, aht_correct=self.aht_correct,
                                          aht_wrong=self.aht_wrong,
                                          netto_contact_rate=self.netto_contract_rate,
                                          right_person_contact_rate=self.right_person_contact_rate)
        self.assertTrue(isinstance(volume, list))
        print(volume)
        self.assertEqual(volume[0], 19.999999999999996)
        self.assertEqual(volume[1], 7.843137254901961)
