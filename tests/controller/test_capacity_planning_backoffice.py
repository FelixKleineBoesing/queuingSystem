import unittest

from src.controller.capacity_planning_backoffice import BackOfficeController


class BackOfficeControllerTester(unittest.TestCase):

    interval = [1800, 1800]
    backlog_sums = [33, 44]
    occupancy = [0.9, 0.8]
    lambdas = [[3, 3, 6, 6, 7, 7, 7, 8, 8, 4, 4, 3, 3, 5, 6, 9, 9, 9, 7, 7],
               [3, 3, 6, 6, 7, 7, 7, 8, 8, 4, 4, 3, 3, 5, 6, 9, 9, 9, 7, 7]]
    ahts = [[190, 190, 190, 190, 220, 220, 220, 220, 220, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190],
            [190, 190, 190, 190, 220, 220, 220, 220, 220, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190, 190]]
    number_agents = [[0.9969135802469136, 0.9969135802469136, 1.3487654320987656, 1.3487654320987656,
                      1.6975308641975306, 1.6975308641975306, 0.9506172839506172, 1.0864197530864197,
                      1.0864197530864197, 0.4691358024691358, 0.4691358024691358, 0.3518518518518519,
                      0.3518518518518519, 0.5864197530864198, 0.7037037037037038, 1.0555555555555556,
                      1.0555555555555556, 1.0555555555555556, 0.8209876543209875, 0.8209876543209875],
                     [1.5569444444444442, 1.5569444444444442, 1.952777777777778, 1.952777777777778, 2.4138888888888883,
                      1.0694444444444444, 1.0694444444444444, 1.222222222222222, 1.222222222222222, 0.5277777777777778,
                      0.5277777777777778, 0.39583333333333337, 0.39583333333333337, 0.6597222222222222,
                      0.7916666666666667, 1.1875, 1.1875, 1.1875, 0.9236111111111109, 0.9236111111111109]]
    backlog_within = [6, 5]
    lambdas_with_backlog = [[a + ((bls / blw) if i < blw else 0) for i, a in enumerate(l)] for l, blw, bls in
                            zip(lambdas, backlog_within, backlog_sums)]

    def test_get_number_agents(self):
        controller = BackOfficeController()
        number_agents = controller.get_number_agents(interval=self.interval, volume=self.lambdas, aht=self.ahts,
                                                     backlog_within=self.backlog_within, occupancy=self.occupancy,
                                                     backlog_sum=self.backlog_sums)
        self.assertTrue(isinstance(number_agents, list))
        for i in range(len(number_agents)):
            for j in range(len(number_agents[i])):
                self.assertAlmostEqual(number_agents[i][j], self.number_agents[i][j], places=7)
        print(number_agents)

    def test_get_volume(self):
        controller = BackOfficeController()
        volume = controller.get_volume(interval=self.interval, number_agents=self.number_agents, aht=self.ahts,
                                       backlog_within=self.backlog_within, occupancy=self.occupancy)
        self.assertTrue(isinstance(volume, list))
        for i in range(len(volume)):
            for j in range(len(volume[i])):
                self.assertAlmostEqual(volume[i][j], self.lambdas_with_backlog[i][j], places=7)
