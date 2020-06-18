from scipy.stats import gamma

from src.modelling.capacity_planning.erlang.optimizer import Optimizer
from src.modelling.helpers import power_faculty


class ErlangA(Optimizer):

    """
    erlang c but with patience and finite size of waiting roomm
    """
    @staticmethod
    def get_max_waiting_probability(lambda_: float, mu: float, nu: float, number_agents: int,
                                    max_waiting_time: int, size_waiting_room: int = None) -> float:
        """
        get the probability that a customer must wait less than the maximum waiting time.
        This is often used as a service level since it displays the probability that a customer could  be satisfied

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param max_waiting_time: maximum waiting time until customers leave
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert nu > 0
        assert number_agents > 0
        assert size_waiting_room > 0
        if size_waiting_room is None:
            size_waiting_room = 1000
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

    @staticmethod
    def get_prob_for_abort(lambda_: float, mu: float, nu: float, number_agents: int,
                           size_waiting_room: int = None) -> float:
        """
        calculates the probability that a customer aborts his call.

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        assert lambda_ > 0
        assert number_agents > 0
        assert mu > 0
        assert nu > 0
        assert size_waiting_room > 0
        if size_waiting_room is None:
            size_waiting_room = 1000
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        res = 0
        for n in range(number_agents + 1, size_waiting_room + 1):
            res += nu / lambda_ * (n - number_agents) * prob_zero * \
                   get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents, n=n)
        return res

    @staticmethod
    def get_average_number_customers_in_system(lambda_: float, mu: float, nu: float, number_agents: int,
                                               size_waiting_room: int = None) -> float:
        """
        calculates the average number of customers that are in the system

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        assert lambda_ > 0
        assert number_agents > 0
        assert mu > 0
        assert nu > 0
        assert number_agents > 0
        assert size_waiting_room > 0
        if size_waiting_room is None:
            size_waiting_room = 1000
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        res = 0
        for n in range(1, size_waiting_room + 1):
            res += prob_zero * n * get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu,
                                                           number_agents=number_agents, n=n)
        return res

    @staticmethod
    def get_average_queue_length(lambda_: float, mu: float, nu: float, number_agents: int,
                                 size_waiting_room: int = None) -> float:
        """
        calculates the average queue length

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        assert lambda_ > 0
        assert number_agents > 0
        assert mu > 0
        assert nu > 0
        assert size_waiting_room > 0
        if size_waiting_room is None:
            size_waiting_room = 1000
        prob_zero = get_prob_for_pn_in_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                    size_waiting_room=size_waiting_room, persons_in_system=0)
        res = 0
        for n in range(number_agents + 1, size_waiting_room + 1):
            res += prob_zero * (n - number_agents) * get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu,
                                                                             number_agents=number_agents, n=n)
        return res

    def get_average_waiting_time(self, lambda_: float, mu: float, nu: float, number_agents: int,
                                 size_waiting_room: int = None) -> float:
        """
        calculates the average waiting time

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        assert lambda_ > 0
        assert number_agents > 0
        assert mu > 0
        assert nu > 0
        assert size_waiting_room > 0
        return self.get_average_queue_length(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                             size_waiting_room=size_waiting_room) / lambda_

    def get_average_staying_time(self, lambda_: float, mu: float, nu: float, number_agents: int,
                                 size_waiting_room: int = None) -> float:
        """
        calculates the average time that a customer stays in the system

        :param lambda_: average arrival time in times per second
        :param mu: average supply time in times per second
        :param nu: abort rate in 1/sec (waiting tolerance of 60 sec = 1/ 60 == 0.01666
        :param number_agents: number of available agents
        :param size_waiting_room: size of a waiting room. If None it is infinite
        :return:
        """
        assert lambda_ > 0
        assert mu > 0
        assert nu > 0
        assert number_agents > 0
        assert size_waiting_room > 0
        return self.get_average_number_customers_in_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                           size_waiting_room=size_waiting_room) / lambda_

    def get_number_agents_for_chat(self, lambda_: float, mu: float, nu: float, max_waiting_time: int,
                                   service_level: float, max_sessions: int, share_sequential_work: float,
                                   size_waiting_room: int = None) -> int:
        """

        :param lambda_:
        :param mu:
        :param nu;
        :param max_waiting_time:
        :param service_level
        :param max_sessions:
        :param share_sequential_work:
        :param size_waiting_room:

        :return: number_agents
        """
        assert lambda_ > 0
        assert 0 <= service_level <= 1
        assert mu > 0
        assert nu > 0
        assert max_sessions > 0
        assert 0 <= share_sequential_work <= 1
        assert size_waiting_room > 0
        aht = 1 / lambda_
        kwargs = {"mu": mu, "max_waiting_time": max_waiting_time, "nu": nu,
                  "lambda_": 1 / (aht * share_sequential_work * max(1, (max_sessions - 1)))}
        if size_waiting_room is not None:
            kwargs["size_waiting_room"] = size_waiting_room
        number_agents = self.minimize(self.get_max_waiting_probability,
                                      kwargs=kwargs, optim_argument="number_agents", target_value=service_level)
        return int(number_agents / max_sessions) + 1

    def get_average_waiting_time_for_chat(self, lambda_: float, mu: float, nu: float, number_agents: int,
                                          max_sessions: int, share_sequential_work: float,
                                          size_waiting_room: int = None) -> float:
        """

        :param lambda_:
        :param mu:
        :param nu:
        :param number_agents
        :param max_sessions:
        :param share_sequential_work:
        :param size_waiting_room:

        :return:
        """
        assert lambda_ > 0
        assert number_agents > 0
        assert mu > 0
        assert max_sessions > 0
        assert 0 <= share_sequential_work <= 1
        assert size_waiting_room > 0
        aht = 1 / lambda_
        kwargs = {"mu": mu, "nu": nu, "number_agents": number_agents,
                  "lambda_": 1 / (aht * share_sequential_work * max(1, (max_sessions - 1)))}
        if size_waiting_room is not None:
            kwargs["size_waiting_room"] = size_waiting_room
        average_waiting_time = self.get_average_waiting_time(**kwargs)
        return average_waiting_time / max_sessions

    get_average_waiting_time_for_chat.return_variable = "asa"
    get_number_agents_for_chat.return_variable = "number_agents"
    get_average_staying_time.return_variable = "average_staying_time"
    get_average_waiting_time.return_variable = "asa"
    get_average_number_customers_in_system.return_variable = "average_number_customers"
    get_max_waiting_probability.return_variable = "abort_prob"
    get_prob_for_abort.return_variable = "abort_prob"
    get_average_queue_length.return_variable = "average_queue_length"


def get_prob_for_pn_in_mmckm_system(lambda_: float, mu: float, nu: float, number_agents: int, size_waiting_room: int,
                                    persons_in_system: int) -> float:
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
            return 0.0
        else:
            return get_cn_for_mmckm_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                           n=persons_in_system) * prob_zero


def get_cn_for_mmckm_system(lambda_: float, mu: float, nu: float, number_agents: int, n: int) -> float:
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
            div = (number_agents * mu + i * nu)
            if div != 0.0:
                res *= lambda_ / div
        return res


if __name__ == "__main__":
    erlang = ErlangA()
    print(erlang.get_max_waiting_probability(lambda_=50/900, mu=1/200, number_agents=19, max_waiting_time=10, nu=1/10000))
    print(erlang.get_max_waiting_probability(lambda_=50/900, mu=1/180, nu=1/1000, number_agents=14,
                                             max_waiting_time=10))
    erlang.plot_cost_function(method=erlang.get_max_waiting_probability,
                              kwargs=dict(number_agents=13, mu=1/180, nu=1/180, size_waiting_room=80, max_waiting_time=20),
                              optim_argument="lambda_", target_value=0.8633721956843062,
                              boundaries=(0, 2), steps=2000).show()
    print(erlang.get_max_waiting_probability(lambda_=50/900, mu=1/180, nu=1/180, number_agents=14, max_waiting_time=10))
    print(erlang.get_max_waiting_probability(lambda_=1/10, mu=1/240, nu=1/300, number_agents=28, size_waiting_room=80,
                                             max_waiting_time=20))
    print(erlang.minimize(method=erlang.get_max_waiting_probability,
                          kwargs=dict(lambda_=1/10, mu=1/240, nu=1/300, size_waiting_room=80, max_waiting_time=20),
                          optim_argument="number_agents", target_value=0.8633721956843062))
    print(erlang.minimize(method=erlang.get_max_waiting_probability,
                          kwargs=dict(lambda_=50/900, mu=1/180, nu=1/180, size_waiting_room=80, max_waiting_time=20),
                          optim_argument="number_agents", target_value=0.8633721956843062))

    print(erlang.get_prob_for_abort(lambda_=1/10, mu=1/240, nu=1/30, number_agents=25, size_waiting_room=80))
    print(erlang.get_average_queue_length(lambda_=1 / 10, mu=1 / 240, nu=1 / 300, number_agents=28, size_waiting_room=80))
    print(erlang.get_average_number_customers_in_system(lambda_=1 / 10, mu=1 / 240, nu=1 / 300, number_agents=28,
                                                        size_waiting_room=80))
    print(erlang.get_average_waiting_time(lambda_=1 / 10, mu=1 / 240, nu=1 / 300, number_agents=28,
                                          size_waiting_room=80))
    print(erlang.get_average_staying_time(lambda_=1 / 10, mu=1 / 240, nu=1 / 300, number_agents=28,
                                          size_waiting_room=80))
    res = erlang.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, max_waiting_time=20, nu=0.05/3,
                                            abort_prob=0.2, max_sessions=2, share_sequential_work=0.15)
    print(res)