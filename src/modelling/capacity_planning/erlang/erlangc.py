import math

from src.modelling.capacity_planning.erlang.optimizer import Optimizer
from src.modelling.helpers import power_faculty


class ErlangC(Optimizer):

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int) \
            -> float:
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

    @staticmethod
    def get_blocking_probability(lambda_: float, mu: float, number_agents: int) -> float:
        """
        get the probability that a customer must wait the maximum waiting time

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :return:
        """
        workload = lambda_ / mu
        p_zero = get_p0_for_mmc_system(workload=workload, number_agents=number_agents)
        if p_zero != 0 and number_agents - workload != 0:
            return power_faculty(workload, number_agents) * number_agents / (number_agents - workload) * p_zero
        else:
            return 0.0

    def get_mean_queue_length(self, lambda_: float, mu: float, number_agents: int) -> float:
        """
        calculates the average queue length

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        workload = lambda_ / mu
        return int(self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) * workload / \
               (number_agents - workload)) + 1

    def get_mean_number_customers_in_system(self, lambda_: float, mu: float, number_agents: int) -> int:
        """
        calculates the mean number of customers in the system based on the workload and number of agents
        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        return int(self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) / \
               (number_agents * mu - lambda_)) + 1

    def get_mean_waiting_time(self, lambda_: float, mu: float, number_agents: int) -> float:
        """
        calculates the mean waiting time

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        if (number_agents * mu - lambda_) == 0.0:
            return 0.0
        else:
            return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) / \
                   (number_agents * mu - lambda_) + 1 / mu

    def get_number_agents_for_chat(self, lambda_: float, mu: float, max_waiting_time: int, abort_prob: float,
                                   max_sessions: int, share_sequential_work: float):
        """

        :param lambda_:
        :param mu:
        :param max_waiting_time:
        :param max_sessions:
        :param share_sequential_work:
        :return:
        """
        aht = 1 / lambda_
        number_agents = self.minimize(self.get_max_waiting_probability,
                                      kwargs={"mu": mu, "max_waiting_time": max_waiting_time,
                                              "lambda_": 1 / (aht * share_sequential_work * (max_sessions - 1))},
                                      optim_argument="number_agents", target_value=abort_prob)
        return number_agents / max_sessions


def get_p0_for_mmc_system(workload: float, number_agents: int):
    result = 0
    for i in range(number_agents):
        result += power_faculty(workload, i)
    if number_agents - workload != 0.0:
        result += power_faculty(workload, number_agents) * number_agents / (number_agents - workload)

    if result > 0:
        return 1 / result
    else:
        return 0


if __name__ == "__main__":
    erlang = ErlangC()
    res = erlang.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, max_waiting_time=20,
                                      abort_prob=0.2, max_sessions=2, share_sequential_work=0.15)
    print(res)
    print(erlang.get_max_waiting_probability(lambda_=50/900, mu=1/180, number_agents=14, max_waiting_time=10))