import unittest

from src.controller.capacity_planning.single_skill.backoffice import BackOfficeController
from tests.capacity_arguments import BackOfficeArguments


class BackOfficeControllerTester(unittest.TestCase, BackOfficeArguments):

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
