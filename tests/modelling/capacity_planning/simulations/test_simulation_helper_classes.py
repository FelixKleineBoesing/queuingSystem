import unittest

from src.modelling.capacity_planning.simulations.queuing import Worker


class WorkerTester(unittest.TestCase):

    def test_construction(self):
        worker = Worker(work_begin=8*60*60, work_end=22*60*60, ahts=[180])

