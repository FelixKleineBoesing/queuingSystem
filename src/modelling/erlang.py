import numpy as np
import math
from src.modelling.helpers import power_faculty, get_p0_for_mmc_system


class ErlangB:

    def get_probability(self, number_agents: int, lambda_: float, mu: float):
        """
        calculates the probability that there are c number people in the system

        :param number_agents: number of available agents
        :param workload: lambda / mu
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


class ErlangC:

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int):
        """
        get the probability that a customer must wait the maximum waiting time

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :return:
        """
        workload = lambda_ / mu

        if workload >= number_agents:
            return 0
        else:
            return 1 - self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) * \
                   math.exp(-(number_agents - workload) * mu * max_waiting_time)

    def get_blocking_probability(self, lambda_: float, mu: float, number_agents: int):
        """
        get the probability that a customer must wait the maximum waiting time

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :return:
        """
        workload = lambda_ / mu
        return power_faculty(workload, number_agents) * number_agents / (number_agents - workload) * \
               get_p0_for_mmc_system(workload=workload, number_agents=number_agents)


if __name__ == "__main__":
    print(power_faculty(10, 2))
    erlang = ErlangB()
    print(erlang.get_probability(9, 21, 3))

    erlang = ErlangC()
    print(erlang.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=35, max_waiting_time=20))
