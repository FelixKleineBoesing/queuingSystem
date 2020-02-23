import unittest
import numpy as np

from src.modelling.erlang import ErlangB, ErlangC


class ErlangBTester(unittest.TestCase):

    def test_erlangb_construction(self):
        erlang = ErlangB()

    def test_get_probability(self):
        prob = self.get_prob(number_agents=1, lambda_=15, mu=3)
        self.assertEqual(prob, 0.8333333333333334)

        prob = self.get_prob(number_agents=10, lambda_=100, mu=5)
        self.assertEqual(prob, 0.5379631686320729)

        prob = self.get_prob(number_agents=190, lambda_=150, mu = 0.75)
        self.assertEqual(prob, 0.08869684386923561)

        prob = self.get_prob(number_agents=200, lambda_=30, mu=6)
        self.assertEqual(prob, 5.31667137954674e-238)

        prob = self.get_prob(number_agents=1000, lambda_=1000, mu=2)
        self.assertEqual(prob, 1.6524151277513355e-86)

        prob = self.get_prob(number_agents=5000, lambda_=10000, mu=1)
        self.assertTrue(np.isnan(prob))

    def get_prob(self, number_agents: int, lambda_: float, mu: float):
        erlang = ErlangB()
        return erlang.get_probability(number_agents=number_agents, lambda_=lambda_, mu=mu)


class ErlangCTester(unittest.TestCase):

    def test_erlangb_construction(self):
        erlang = ErlangC()

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int):
        erlang = ErlangC()
        return erlang.get_max_waiting_probability(lambda_=lambda_, mu=mu, number_agents=number_agents,
                                                  max_waiting_time=max_waiting_time)

    def test_get_max_waiting_probability(self):
        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 0.7710233599946846)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=135, max_waiting_time=10)
        self.assertEqual(prob, 1)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.133, number_agents=50, max_waiting_time=200)
        self.assertEqual(prob, 1)

        prob = self.get_max_waiting_probability(lambda_=1, mu=0.0038, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 0)

        prob = self.get_max_waiting_probability(lambda_=10, mu=0.12, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 0)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=3.0033, number_agents=35, max_waiting_time=20)
        self.assertEqual(prob, 1.0)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=40, max_waiting_time=20)
        self.assertEqual(prob, 0.9668921807646333)

        prob = self.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=20, max_waiting_time=20)
        self.assertEqual(prob, 0)