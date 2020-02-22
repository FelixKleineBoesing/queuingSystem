import unittest
from src.modelling.helpers import power_faculty


class ModellingHelpersTester(unittest.TestCase):

    def test_power_faculty(self):
        var = (1, 2)
        result = power_faculty(*var)
        self.assertEqual(result, 0.5)

        var = (5, 7)
        result = power_faculty(*var)
        self.assertEqual(result, 15.500992063492061)

        var = (3, 10)
        result = power_faculty(*var)
        self.assertEqual(result, 0.016272321428571428)

        var = (50, 100)
        result = power_faculty(*var)
        self.assertEqual(result, 845272575844.2825)

        var = (50, 3)
        result = power_faculty(*var)
        self.assertEqual(result, 20833.333333333332)