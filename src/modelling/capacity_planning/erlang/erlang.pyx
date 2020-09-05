

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
    cdef float prob_zero = 0
    number_agents = int(number_agents)

    cdef int i
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
    cdef float a = lambda_ / mu
    cdef int i
    cdef float div
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

def power_faculty(x: float, n: float) -> float:
    cdef float result = 1
    cdef int i
    for i in range(1, int(n + 1)):
        result = result * x / i
    return result
