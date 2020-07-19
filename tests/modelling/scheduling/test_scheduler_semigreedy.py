import unittest
import numpy as np
import datetime
from src.modelling.scheduler.scheduler_semi_greedy import SchedulerSemiGreedy


class SchedulerSemiGreedyTester(unittest.TestCase):

    def setUp(self) -> None:
        self.agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                                12, 12, 7, 10, 7]

    def test_construction(self):
        scheduler = SchedulerSemiGreedy(demands=self.agents_per_hour, lunch_time=1,
                                        number_intervals_per_agent=17, lunch_time_border=6)
        self.assertEqual(scheduler.demands, self.agents_per_hour)
        self.assertEqual(scheduler.lunch_time, 1)
        self.assertEqual(scheduler.number_intervals_per_agent, 17)
        self.assertEqual(scheduler.lunch_time_border, 6)

    def test_solve(self):
        start = datetime.datetime.now()
        scheduler = SchedulerSemiGreedy(demands=self.agents_per_hour, lunch_time=1,
                                        number_intervals_per_agent=17, lunch_time_border=6, verbose=False)
        shifts = scheduler.solve()
        duration = datetime.datetime.now() - start
        print(duration.total_seconds())
        print(np.sum(shifts, axis=1).tolist())
        self.assertEqual(np.sum(shifts, axis=1).tolist(), [12.0, 12.0, 13.0, 13.0, 15.0, 24.0, 23.0, 33.0, 36.0, 40.0,
                                                           32.0, 50.0, 46.0, 47.0, 40.0, 41.0, 45.0, 38.0, 38.0, 37.0,
                                                           35.0, 30.0, 26.0, 26.0, 17.0, 14.0, 10.0, 7.0])

        self.assertTrue(duration.total_seconds() < 0.200, "Solve took longer than 200 milliseonds. "
                                                          "There must be something wrong with the algorithm!")

    def test_check_number_of_lunch_times_to_assign(self):
        shifts = np.array([[1, 1, 1, 1, 1, 0, 0, 0], [0, 2, 2, 2, 2, 2, 0, 0], [0, 0, 4, 4, 4, 4, 4, 0]]).transpose()
        scheduler = SchedulerSemiGreedy(demands=self.agents_per_hour, lunch_time=1,
                                        number_intervals_per_agent=5, lunch_time_border=1, verbose=False)
        number_necessary_lunch_times = scheduler._check_number_of_lunch_times_to_assign(shifts=shifts)
        self.assertTrue(isinstance(number_necessary_lunch_times, np.ndarray))
        self.assertTrue(number_necessary_lunch_times.tolist(), [1, 2, 4])

        shifts = np.array([[1, 1, 1, 0, 1, 0, 0, 0], [0, 2, 2, 0, 2, 2, 0, 0], [0, 0, 4, 4, 3, 1, 4, 0]]).transpose()
        scheduler = SchedulerSemiGreedy(demands=self.agents_per_hour, lunch_time=1,
                                        number_intervals_per_agent=5, lunch_time_border=1, verbose=False)
        number_necessary_lunch_times = scheduler._check_number_of_lunch_times_to_assign(shifts=shifts)
        self.assertTrue(isinstance(number_necessary_lunch_times, np.ndarray))
        self.assertTrue(number_necessary_lunch_times.tolist(), [0, 0, 0])

    def test_check_lunch_time_constraint(self):
        shifts = np.array([[1, 1, 1, 1, 1, 0, 0, 0], [0, 2, 2, 2, 2, 2, 0, 0], [0, 0, 4, 4, 4, 4, 4, 0]]).transpose()
        scheduler = SchedulerSemiGreedy(demands=self.agents_per_hour, lunch_time=1,
                                        number_intervals_per_agent=5, lunch_time_border=1, verbose=False)
        satisfied = scheduler._check_lunch_time_constraint(shifts=shifts)
        self.assertFalse(satisfied)

        shifts = np.array([[1, 1, 1, 0, 1, 0, 0, 0], [0, 2, 2, 0, 2, 2, 0, 0], [0, 0, 4, 4, 3, 1, 4, 0]]).transpose()
        scheduler = SchedulerSemiGreedy(demands=self.agents_per_hour, lunch_time=1,
                                        number_intervals_per_agent=5, lunch_time_border=1, verbose=False)
        satisfied = scheduler._check_lunch_time_constraint(shifts=shifts)
        self.assertTrue(satisfied)