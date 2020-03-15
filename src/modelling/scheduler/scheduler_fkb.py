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
        demand = np.array(self.number_agents_per_half_hour)
        j = 0
        for i in range(len(self.number_agents_per_half_hour)):
            condition_met = all(demand <= np.sum(self._data, axis=1))
            service_ineffiecency = 1 - (sum(self.number_agents_per_half_hour) / np.sum(self._data))
            print("Service Inefficiency is : {}".format(service_ineffiecency))
            print("Condition met: {}".format(condition_met))
            sum_agents = np.sum(self._data[i, :])
            if sum_agents < self.number_agents_per_half_hour[i]:
                self._data[i:i+self.number_intervals_per_agent, j] = self.number_agents_per_half_hour[i] - sum_agents
                j += 1


        # TODO add lunch time
        # TODO add part times

        print(np.sum(self._data, axis=1))

    def solve(self):
        pass


if __name__ == "__main__":
    agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                       12, 12, 7, 10, 7]
    scheduler = SchedulerFKB(number_agents_per_half_hour=agents_per_hour, lunch_time=1,
                             number_intervals_per_agent=17)
    scheduler.solve()
