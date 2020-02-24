import math

from src.modelling.helpers import power_faculty, get_p0_for_mmc_system


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

    def get_mean_queue_length(self, lambda_: float, mu: float, number_agents: int):
        """
        calculates the average queue length

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        workload = lambda_ / mu
        return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) * workload / \
               (number_agents - workload)

    def get_mean_number_customers_in_system(self, lambda_: float, mu: float, number_agents: int):
        """
        calculates the mean number of customers in the system based on the workload and number of agents
        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) / \
               (number_agents * mu - lambda_)

    def get_mean_waiting_time(self, lambda_: float, mu: float, number_agents: int):
        """
        calculates the mean waiting time

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) / \
               (number_agents * mu - lambda_) + 1 / mu
