import unittest
from src.modelling.helpers import power_faculty
from src.modelling.capacity_planning.erlang.erlangc import get_p0_for_mmc_system


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

    def test_get_p0_for_mmc_system(self):
        prob = get_p0_for_mmc_system(5, 1)
        self.assertEqual(prob, 0)

        prob = get_p0_for_mmc_system(3, 16)
        self.assertEqual(prob, 0.04978706826876853)

        prob = get_p0_for_mmc_system(2, 25)
        self.assertEqual(prob, 0.13533528323661273)

        prob = get_p0_for_mmc_system(5, 38)
        self.assertEqual(prob, 0.00673794699908547)

        prob = get_p0_for_mmc_system(3, 99)
        self.assertEqual(prob, 0.04978706836786396)

        prob = get_p0_for_mmc_system(15, 153)
        self.assertEqual(prob, 3.059023205018257e-07)