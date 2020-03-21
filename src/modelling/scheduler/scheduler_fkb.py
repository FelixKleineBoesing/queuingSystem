import logging

import numpy as np
from src.modelling.scheduler.scheduler_base import Scheduler


class SchedulerFKB(Scheduler):

    def __init__(self, number_agents_per_half_hour: list, lunch_time: int = 1, lunch_time_border: int = 6,
                 number_intervals_per_agent: int = 17):
        """

        :param number_agents_per_half_hour: a list of demands for agents
        :param lunch_time: the length of the lunch
        :param lunch_time_border: describes the distance that a lunch must have from beginning and end of a shift
        :param number_intervals_per_agent: the number of intervals that an agent has to work
        """
        super().__init__(number_intervals_per_agent=number_intervals_per_agent,
                         number_agents_per_half_hour=number_agents_per_half_hour,
                         lunch_time=lunch_time)
        self._data = None
        self._build_model()

    def _build_model(self):
        self._data = np.zeros((len(self.number_agents_per_half_hour), len(self.number_agents_per_half_hour)))

    def solve(self):
        demand = np.array(self.number_agents_per_half_hour)
        j = 0
        for i in range(len(self.number_agents_per_half_hour)):
            condition_met = all(demand <= np.sum(self._data, axis=1))
            service_ineffiecency = self.get_service_efficiency(demand, self._data)
            print("Service Inefficiency is : {}".format(service_ineffiecency))
            print("Condition met: {}".format(condition_met))
            sum_agents = np.sum(self._data[i, :])
            if sum_agents < self.number_agents_per_half_hour[i] and \
                    i <= self._data.shape[0] - self.number_intervals_per_agent:
                self._data[i:i + self.number_intervals_per_agent, j] = self.number_agents_per_half_hour[i] - sum_agents
                j += 1
            else:
                if np.sum(self._data[i, :]) < self.number_agents_per_half_hour[i]:
                    condition_met = False
                    while not condition_met:
                        self._data = self._get_optimal_next_shift(demands=demand, shifts=self._data)
                        self.get_service_efficiency(demand, self._data)
                        print(i)
                        if np.sum(self._data[i, :]) >= self.number_agents_per_half_hour[i]:
                            condition_met = True
        # TODO add lunch time
        # TODO add part times
        return self._data

    def _get_optimal_next_shift(self, demands: np.ndarray, shifts: np.ndarray):
        shifts = shifts.copy()
        results = []
        shift_sums = np.sum(shifts, axis=0)
        for i in range(shifts.shape[0]):
            if shift_sums[i] > 0:
                service_inefficiency = self._get_service_inefficiency_by_condition(shifts=shifts, demands=demands,
                                                                                   column=i, indices=shifts[:, i] > 0)
                results.append(service_inefficiency)
            else:
                results.append(np.NaN)

        if np.all(~np.isfinite(results)):
            results = []
            column = self._get_free_shift(shifts=shifts)
            for i in range(shifts.shape[0]):
                if i <= self._data.shape[0] - self.number_intervals_per_agent:
                    indices = list(range(i, i + self.number_intervals_per_agent))
                    service_inefficiency = self._get_service_inefficiency_by_condition(shifts=shifts, demands=demands,
                                                                                       column=column, indices=indices)
                    results.append(service_inefficiency)
                else:
                    results.append(np.NaN)
            index = np.nanargmin(results)
            shifts[index:index+self.number_intervals_per_agent, column] = \
                shifts[index:index+self.number_intervals_per_agent, column] + 1
        else:
            index = np.nanargmin(results)
            shifts[shifts[:, index] > 0, index] = shifts[shifts[:, index] > 0, index] + 1
        return shifts

    def _get_free_shift(self, shifts: np.ndarray):
        """
        return the index of a column where no shift is assigned

        :param shifts:
        :return:
        """
        for i in range(shifts.shape[1]):
            if np.all(shifts[:, i] == 0):
                return i

    def _get_service_inefficiency_by_condition(self, shifts, demands, column, indices :list):
        """
        divides the service inefficiency by the number of demand that can be covered additionaly

        :return:
        """
        tmp = shifts.copy()
        tmp[indices, column] = tmp[indices, column] + 1
        service_inefficiency = self.get_service_efficiency(demands, tmp)
        condition = np.logical_and.reduce((np.sum(shifts, axis=1) < demands, np.sum(tmp, axis=1) <= demands,
                                           np.sum(shifts, axis=1) < np.sum(tmp, axis=1)))
        return service_inefficiency / np.sum(condition)

    @staticmethod
    def get_service_efficiency(demands: np.ndarray, shifts: np.ndarray):
        return 1 - (sum(demands) / np.sum(shifts))


if __name__ == "__main__":
    agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                       12, 12, 7, 10, 7]
    agents_excel_sheet = [12, 12, 14, 21, 28, 22, 33, 36, 40, 41, 50, 50, 35, 46, 50, 50,
                          34, 38, 33, 26, 22, 21, 17, 17, 14, 10, 7]

    scheduler = SchedulerFKB(number_agents_per_half_hour=agents_per_hour, lunch_time=1,
                             number_intervals_per_agent=17)
    print(scheduler.get_service_efficiency(demands=agents_per_hour, shifts=agents_excel_sheet))
    shifts = scheduler.solve()
    print(np.sum(shifts, axis=1))
