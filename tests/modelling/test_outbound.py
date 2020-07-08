import unittest

from src.modelling.capacity_planning.outbound.outbound import OutboundCalculator


class OutboundCalculatorTester(unittest.TestCase):

    lambdas = [20 / 1800, 40 / 600]
    dialing_time = [1 / 5, 1 / 10]
    netto_contact_rate = [0.9, 0.85]
    right_person_contact_rate = [0.8, 0.75]
    mu_correct = [1 / 200, 1 / 170]
    mu_wrong = [1 / 15, 1 / 170]
    number_agents = [1.6800000000000004, 10.2]

    def test_get_number_agents(self):
        outbound = OutboundCalculator()
        number_agents = outbound.get_number_agents(lambda_=self.lambdas[0], dialing_time=self.dialing_time[0],
                                                   netto_contact_rate=self.netto_contact_rate[0],
                                                   right_person_contact_rate=self.right_person_contact_rate[0],
                                                   mu_correct=self.mu_correct[0], mu_wrong=self.mu_wrong[0])
        self.assertTrue(isinstance(number_agents, float))
        self.assertAlmostEqual(number_agents, 1.6800000000000004, places=8)

        number_agents = outbound.get_number_agents(lambda_=self.lambdas[1], dialing_time=self.dialing_time[1],
                                                   netto_contact_rate=self.netto_contact_rate[1],
                                                   right_person_contact_rate=self.right_person_contact_rate[1],
                                                   mu_correct=self.mu_correct[1], mu_wrong=self.mu_wrong[1])
        self.assertTrue(isinstance(number_agents, float))
        self.assertAlmostEqual(number_agents, 10.2, places=8)

    def test_get_volume(self):
        outbound = OutboundCalculator()
        volume = outbound.get_volume(dialing_time=self.dialing_time[0], netto_contact_rate=self.netto_contact_rate[0],
                                     right_person_contact_rate=self.right_person_contact_rate[0],
                                     mu_correct=self.mu_correct[0], mu_wrong=self.mu_wrong[0],
                                     number_agents=self.number_agents[0])
        self.assertTrue(isinstance(volume, float))
        self.assertAlmostEqual(volume, self.lambdas[0])

        volume = outbound.get_volume(dialing_time=self.dialing_time[1], netto_contact_rate=self.netto_contact_rate[1],
                                     right_person_contact_rate=self.right_person_contact_rate[1],
                                     mu_correct=self.mu_correct[1], mu_wrong=self.mu_wrong[1],
                                     number_agents=self.number_agents[1])
        self.assertTrue(isinstance(volume, float))
        self.assertAlmostEqual(volume, self.lambdas[1])