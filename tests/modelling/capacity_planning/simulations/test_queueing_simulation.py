import unittest

from src.modelling.capacity_planning.simulations.queuing import System


class QueueingSimulationTester(unittest.TestCase):

    def test_construction(self):
        callcenter = System()