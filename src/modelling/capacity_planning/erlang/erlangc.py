import math

from src.modelling.capacity_planning.erlang.optimizer import Optimizer
from src.modelling.helpers import power_faculty


class ErlangC(Optimizer):

    def get_max_waiting_probability(self, lambda_: float, mu: float, number_agents: int, max_waiting_time: int) \
            -> float:
        """
        get the probability that a customer must wait less than the maximum waiting time

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert max_waiting_time > 0
        assert number_agents > 0
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
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert number_agents > 0
        workload = lambda_ / mu
        p_zero = get_p0_for_mmc_system(workload=workload, number_agents=number_agents)
        if p_zero != 0 and number_agents - workload != 0:
            return power_faculty(workload, number_agents) * number_agents / (number_agents - workload) * p_zero
        else:
            return 0.0

    def get_average_queue_length(self, lambda_: float, mu: float, number_agents: int) -> float:
        """
        calculates the average queue length

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert number_agents > 0
        workload = lambda_ / mu
        return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) * workload / \
                   (number_agents - workload)

    def get_average_number_customers_in_system(self, lambda_: float, mu: float, number_agents: int) -> float:
        """
        calculates the mean number of customers in the system based on the workload and number of agents
        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert number_agents > 0
        workload = lambda_ / mu
        return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) * workload / \
                   (number_agents - workload) + workload

    def get_average_waiting_time(self, lambda_: float, mu: float, number_agents: int) -> float:
        """
        calculates the mean waiting time

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert number_agents > 0
        if (number_agents * mu - lambda_) == 0.0:
            return 0.0
        else:
            return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) / \
                   (number_agents * mu - lambda_)

    def get_average_staying_time(self, lambda_: float, mu: float, number_agents: int) -> float:
        """
        calculates the mean waiting time

        :param lambda_:
        :param mu:
        :param number_agents:
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert number_agents > 0
        if (number_agents * mu - lambda_) == 0.0:
            return 0.0
        else:
            return self.get_blocking_probability(lambda_=lambda_, mu=mu, number_agents=number_agents) / \
                   (number_agents * mu - lambda_) + 1 / mu

    def get_number_agents_for_chat(self, lambda_: float, mu: float, max_waiting_time: int, service_level: float,
                                   max_sessions: int, share_sequential_work: float):
        """

        :param lambda_:
        :param mu:
        :param max_waiting_time:
        :param service_level
        :param max_sessions:
        :param share_sequential_work:
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert max_waiting_time > 0
        assert max_sessions > 0
        assert 0 <= service_level <= 1
        assert 0 <= share_sequential_work <= 1
        aht = 1 / lambda_
        number_agents = self.minimize(self.get_max_waiting_probability,
                                      kwargs={"mu": mu, "max_waiting_time": max_waiting_time,
                                              "lambda_": 1 / (aht * share_sequential_work * max(1, (max_sessions - 1)))},
                                      optim_argument="number_agents", target_value=service_level)
        return int(number_agents / max_sessions) + 1

    def get_average_waiting_time_for_chat(self, lambda_: float, mu: float, max_sessions: int, number_agents: int,
                                          share_sequential_work: float):
        """

        :param lambda_:
        :param mu:
        :param max_sessions:
        :param share_sequential_work:
        :return:
        """
        assert lambda_ > 0
        assert number_agents > 0
        assert mu > 0
        assert max_sessions > 0
        assert 0 <= share_sequential_work <= 1
        aht = 1 / lambda_
        kwargs = {"mu": mu,  "lambda_": 1 / (aht * share_sequential_work * max(1, (max_sessions - 1))),
                  "number_agents": number_agents}
        average_waiting_time = self.get_average_waiting_time(**kwargs)
        return average_waiting_time / max_sessions

    get_average_waiting_time_for_chat.return_variable = "asa"
    get_number_agents_for_chat.return_variable = "number_agents"
    get_average_waiting_time.return_variable = "asa"
    get_average_number_customers_in_system.return_variable = "average_number_customers"
    get_max_waiting_probability.return_variable = "abort_prob"
    get_blocking_probability.return_variable = "blocking_probability"
    get_average_queue_length.return_variable = "average_queue_length"


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
    print(erlang.get_blocking_probability(7, 1, 9))

    res = erlang.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, max_waiting_time=20,
                                            service_level=0.8, max_sessions=2, share_sequential_work=0.15)
    print(res)
    print(erlang.get_max_waiting_probability(lambda_=50/900, mu=1/200, number_agents=14, max_waiting_time=10))
    print(erlang.minimize(erlang.get_average_waiting_time_for_chat,
                              kwargs={'lambda_': 0.05555555555555555, 'mu': 0.005555555555555556,
                                      'share_sequential_work': 0.15, 'max_sessions': 5},
                              target_value=50,  optim_argument="number_agents"))