import unittest
from src.modelling.helpers import power_faculty

class ModellingHelpersTester(unittest.TestCase):

    def test_power_faculty(self):
        var = (1, 2)
        result = power_faculty(*var)
        print(result)