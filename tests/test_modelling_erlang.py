import unittest

from src.modelling.erlang import ErlangB


class ErlangTester(unittest.TestCase):

    def test_erlangb_construction(self):
        erlang = ErlangB(number_agents=1, workload=5)
        self.assertEqual(erlang.a, 5)
        self.assertEqual(erlang.c, 1)

    def test_get_probability(self):
        erlang = ErlangB(number_agents=1, workload=5)
        prob = erlang.get_probability()
        self.assertEqual(prob, 0.1)

