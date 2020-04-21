from scipy.stats import gamma
from scipy.optimize import minimize_scalar

from src.modelling.erlang.optimizer import Optimizer
from src.modelling.helpers import power_faculty


class ErlangCP(Optimizer):

    """
    erlang c but with patience and finite size of waiting roomm
    """

    def get_service_level(self, lambda_: float, mu: float, nu: float, number_agents: int,
                          max_waiting_time: int, size_waiting_room: int = None):
        """
        gets the service level by subtracting the max_waiting_probabilty from one

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        return 1 - self.get_max_waiting_probability(lambda_, mu, nu, number_agents, max_waiting_time, size_waiting_room)

    def get_max_waiting_probability(self, lambda_: float, mu: float, nu: float, number_agents: int,
                                    max_waiting_time: int, size_waiting_room: int = None):
        """
        get the probability that a customer must wait the maximum waiting time. This is often used as a service level
        since it displays the probability that a customer could not be satisfied, when substracted from 1

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        if size_waiting_room is None:
            size_waiting_room = 9e20
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        if prob_zero == 0:
            prob = 1
        else:
            prob = 1 - prob_zero * get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                           n=size_waiting_room)

        for n in range(number_agents, size_waiting_room):
            x = (number_agents * mu + nu) * max_waiting_time
            g = 1 - gamma(a=n - number_agents + 1).cdf(x=x)
            prob = prob - prob_zero * get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu,
                                                              number_agents=number_agents, n=n) * g
        return prob

    def get_prob_for_abort(self,  lambda_: float, mu: float, nu: float, number_agents: int,
                           size_waiting_room: int = None):
        """
        calculates the probability that a customer aborts his call.

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        if size_waiting_room is None:
            size_waiting_room = 9e20
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        res = 0
        for n in range(number_agents + 1, size_waiting_room + 1):
            res += nu / lambda_ * (n - number_agents) * prob_zero * \
                   get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents, n=n)
        return res

    def get_mean_number_customer_in_system(self,  lambda_: float, mu: float, nu: float, number_agents: int,
                                           size_waiting_room: int = None):
        """
        calculates the average number of customers that are in the system

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        if size_waiting_room is None:
            size_waiting_room = 9e20
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        res = 0
        for n in range(1, size_waiting_room + 1):
            res += prob_zero * n * get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu,
                                                           number_agents=number_agents, n=n)
        return res

    def get_mean_queue_length(self,  lambda_: float, mu: float, nu: float, number_agents: int,
                              size_waiting_room: int = None):
        """
        calculates the average queue length

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        if size_waiting_room is None:
            size_waiting_room = 9e20
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        res = 0
        for n in range(number_agents + 1, size_waiting_room + 1):
            res += prob_zero * (n - number_agents) * get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu,
                                                                             number_agents=number_agents, n=n)
        return res

    def get_mean_waiting_time(self,  lambda_: float, mu: float, nu: float, number_agents: int,
                              size_waiting_room: int = None):
        """
        calculates the average waiting time

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        return self.get_mean_queue_length(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                          size_waiting_room=size_waiting_room) / lambda_

    def get_mean_staying_time(self,  lambda_: float, mu: float, nu: float, number_agents: int,
                              size_waiting_room: int = None):
        """
        calculates the average time that a customer stays in the system

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        return self.get_mean_number_customer_in_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                       size_waiting_room=size_waiting_room) / lambda_


def get_prob_for_pn_in_mmckm_system(lambda_: float, mu: float, nu: float, number_agents: int, size_waiting_room: int,
                                    persons_in_system: int):
    """
    calculatzes the probability that there are n persons in a M/M/c/K/m system

    :param lambda_:
    :param mu:
    :param nu:
    :param number_agents:
    :param size_waiting_room:
    :param persons_in_system:
    :return:
    """
    prob_zero = 0
    number_agents = int(number_agents)
    for i in range(size_waiting_room + 1):
        prob_zero += get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents, n=i)

    prob_zero = 1 / prob_zero

    if persons_in_system == 0:
        return prob_zero
    else:
        if persons_in_system > size_waiting_room:
            return 0
        else:
            return get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                           n=persons_in_system) * prob_zero


def get_cn_for_mmckm_system(lambda_: float, mu: float, nu: float, number_agents: int, n: int):
    """


    :param lambda_:
    :param mu:
    :param nu:
    :param number_agents:
    :param n:
    :return:
    """
    a = lambda_ / mu
    number_agents = int(number_agents)
    if n <= number_agents:
        return power_faculty(a, n)
    else:
        res = power_faculty(a, number_agents)
        for i in range(1, n - number_agents + 1):
            res *= lambda_ / (number_agents * mu + i * nu)
        return res


if __name__ == "__main__":
    erlang = ErlangCP()
    print(erlang.get_max_waiting_probability(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28, size_waiting_room=80,
                                             max_waiting_time=20))
    print(erlang.get_service_level(lambda_=1 / 10, mu=1 / 240, nu=1 / 300, number_agents=28,
                                   size_waiting_room=80, max_waiting_time=20))
    print(erlang.minimize(method=erlang.get_max_waiting_probability, kwargs=dict(lambda_=1/10, mu=1/240, nu=1/300,
                                                                                 size_waiting_room=80, max_waiting_time=20),
                          optim_argument="number_agents", target_value=0.8633721956843062))
    print(erlang.get_prob_for_abort(lambda_=1/10, mu=1/240, nu=1/30, number_agents=25, size_waiting_room=80))
    print(erlang.get_mean_queue_length(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28, size_waiting_room=80))
    print(erlang.get_mean_number_customer_in_system(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28,
                                                    size_waiting_room=80))
    print(erlang.get_mean_waiting_time(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28,
                                       size_waiting_room=80))
    print(erlang.get_mean_staying_time(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28,
                                       size_waiting_room=80))