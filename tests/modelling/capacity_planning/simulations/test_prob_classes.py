import unittest
import numpy as np

from src.modelling.capacity_planning.simulations.probability_classes import NormalDistribution, ListDrawer, \
    ExponentialDistribution, KernelDensity, ErlangDistribution, WeibullDistribution


class ProbClassesTester(unittest.TestCase):

    def test_norm_dist(self):
        norm_dist = NormalDistribution(mean=10, sd=5)
        values = norm_dist.draw(10000)
        self.assertAlmostEqual(float(np.mean(values)), 10, delta=0.3)
        self.assertAlmostEqual(float(np.std(values)), 5, delta=0.3)

    def test_list_drawer(self):
        list_drawer = ListDrawer(data=[1, 2, 3, 2, 1, 3])
        values = list_drawer.draw(10000)
        self.assertAlmostEqual(float(np.mean(values)), 2, delta=0.1)

    def test_exp_dist(self):
        exp_dist = ExponentialDistribution(1)
        values = exp_dist.draw(10000)
        self.assertAlmostEqual(float(np.mean(values)), 2, delta=0.2)

    def test_erlang_dist(self):
        erlang_dist = ErlangDistribution(lambda_=2)
        values = erlang_dist.draw(10000)
        self.assertAlmostEqual(float(np.mean(values)), 2, delta=0.05)

    def test_weib_dist(self):
        self.skipTest("not implemented")
        weibull_dist = WeibullDistribution(x=1)
        values = weibull_dist.draw(10000)
        self.assertAlmostEqual(float(np.mean(values)), 2, delta=0.05)
