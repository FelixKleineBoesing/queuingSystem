import unittest

from src.modelling.capacity_planning.backoffice.backoffice import BackOfficeCalculator


class BackOfficeTester(unittest.TestCase):

    backlog_sums = [33/1800, 44/1800]
    occupancy = [0.9, 0.8]
    lambdas = [[3, 3, 6, 6, 7, 7, 7, 8, 8, 4, 4, 3, 3, 5, 6, 9, 9, 9, 7, 7],
               [3, 3, 6, 6, 7, 7, 7, 8, 8, 4, 4, 3, 3, 5, 6, 9, 9, 9, 7, 7]]
    lambdas = [[a / 1800 for a in l] for l in lambdas]
    ahts = [[190, 190, 190, 190, 220, 220, 220, 220, 220, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190],
            [190, 190, 190, 190, 220, 220, 220, 220, 220, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190]]
    number_agents = [[0.9969135802469136, 0.9969135802469136, 1.3487654320987656, 1.3487654320987656,
                      1.6975308641975306, 1.6975308641975306, 1.6975308641975306, 1.0864197530864197,
                      1.0864197530864197, 0.4691358024691358, 0.4691358024691358, 0.3518518518518519,
                      0.3518518518518519, 0.5864197530864198, 0.7037037037037038, 1.0555555555555556,
                      1.0555555555555556, 1.0555555555555556, 0.8209876543209875, 0.8209876543209875],
                     [1.5569444444444442, 1.5569444444444442, 1.952777777777778, 1.952777777777778,
                      2.4138888888888883, 2.4138888888888883, 1.0694444444444444, 1.222222222222222,
                      1.222222222222222, 0.5277777777777778, 0.5277777777777778, 0.39583333333333337,
                      0.39583333333333337, 0.6597222222222222, 0.7916666666666667, 1.1875, 1.1875, 1.1875,
                      0.9236111111111109, 0.9236111111111109]]
    backlog_within = [6, 5]

    def test_get_required_agents(self):
        backoffice = BackOfficeCalculator()
        number_agents = backoffice.get_required_agents(lambdas=self.lambdas[0], ahts=self.ahts[0],
                                                       backlog_sum=self.backlog_sums[0],
                                                       backlog_within=self.backlog_within[0],
                                                       occupancy=self.occupancy[0])
        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(self.number_agents[0], number_agents)

        number_agents = backoffice.get_required_agents(lambdas=self.lambdas[1], ahts=self.ahts[1],
                                                       backlog_sum=self.backlog_sums[1],
                                                       backlog_within=self.backlog_within[1],
                                                       occupancy=self.occupancy[1])

        self.assertTrue(isinstance(number_agents, list))
        self.assertEqual(self.number_agents[1], number_agents)

    def test_get_possible_volume(self):
        backoffice = BackOfficeCalculator()
        volume = backoffice.get_possible_volume(available_agents=self.number_agents[0], ahts=self.ahts[0],
                                                backlog_within=self.backlog_within[0], occupancy=self.occupancy[0])
        print(volume)
        self.assertTrue(isinstance(volume, list))
        self.assertEqual(self.lambdas[0], volume)

        volume = backoffice.get_possible_volume(available_agents=self.number_agents[1], ahts=self.ahts[1],
                                                backlog_within=self.backlog_within[1], occupancy=self.occupancy[1])
        print(volume)
        self.assertTrue(isinstance(volume, list))
        self.assertEqual(self.lambdas[1], volume)

