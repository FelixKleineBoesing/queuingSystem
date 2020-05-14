import numpy as np

from src.modelling.capacity_planning.erlang.optimizer import Optimizer
from src.modelling.helpers import power_faculty


class ErlangB(Optimizer):

    def get_probability(self, number_agents: int, lambda_: float, mu: float):
        """
        calculates the probability that there are c number people in the system

        :param number_agents: number of available agents
        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :return: probability of a blocked queue
        """
        workload = lambda_ / mu
        sum = 0.0
        for i in range(number_agents + 1):
            sum += power_faculty(workload, i)
            if np.isnan(sum):
                break

        return power_faculty(workload, number_agents) / sum