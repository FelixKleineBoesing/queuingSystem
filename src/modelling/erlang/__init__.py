from src.modelling.erlang.erlangb import ErlangB
from src.modelling.erlang.erlangc import ErlangC
from src.modelling.erlang.erlangcp import ErlangCP
from src.modelling.helpers import power_faculty

if __name__ == "__main__":
    # lambda, mu and nu are defined in 1/second. Therefore, lambda= 1/10 means each 10 seconds someone arrives.

    lambda_ = 1/10
    mu = 1/240
    nu = 1/300
    number_agents = 28
    max_waiting_time = 20
    size_waiting_room = 80

    erlangcp = ErlangCP()

    res = erlangcp.get_max_waiting_probability(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                               max_waiting_time=max_waiting_time, size_waiting_room=size_waiting_room)
    print("Probability for a customer waiting the maximum time: {}".format(res))

    res = erlangcp.get_prob_for_abort(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                      size_waiting_room=size_waiting_room)
    print("Probability for call abort: {}".format(res))

    res = erlangcp.get_mean_staying_time(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                         size_waiting_room=size_waiting_room)
    print("average staying time: {}".format(res))

    res = erlangcp.get_mean_waiting_time(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                         size_waiting_room=size_waiting_room)
    print("Average waiting time: {}".format(res))

    res = erlangcp.get_mean_queue_length(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                         size_waiting_room=size_waiting_room)
    print("Avearage queue length: {}".format(res))

    res = erlangcp.get_mean_number_customer_in_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                      size_waiting_room=size_waiting_room)
    print("average number customers in system: {}".format(res))
