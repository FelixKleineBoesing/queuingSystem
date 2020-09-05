

if __name__ == "__main__":
    from src.modelling.capacity_planning.erlang.erlanga import ErlangA
    # lambda, mu and nu are defined in 1/second. Therefore, lambda= 1/10 means each 10 seconds someone arrives.

    lambda_ = 1/10
    mu = 1/240
    nu = 1/300
    number_agents = 28
    max_waiting_time = 20
    size_waiting_room = 80
    target_sla = 0.8633721956843062

    erlangcp = ErlangA()

    res = erlangcp.get_max_waiting_probability(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                               max_waiting_time=max_waiting_time, size_waiting_room=size_waiting_room)
    print("Probability for a customer waiting the maximum time: {}".format(res))

    print(erlangcp.minimize(method=erlangcp.get_max_waiting_probability,
                            kwargs=dict(lambda_=1/10, mu=1/240, nu=1/300, size_waiting_room=80, max_waiting_time=20),
                            optim_argument="number_agents", target_value=0.8633721956843062))

    res = erlangcp.get_prob_for_abort(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                      size_waiting_room=size_waiting_room)
    print("Probability for call abort: {}".format(res))

    res = erlangcp.get_average_staying_time(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                            size_waiting_room=size_waiting_room)
    print("average staying time: {}".format(res))

    res = erlangcp.get_average_waiting_time(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                            size_waiting_room=size_waiting_room)
    print("Average waiting time: {}".format(res))

    res = erlangcp.get_average_queue_length(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                            size_waiting_room=size_waiting_room)
    print("Avearage queue length: {}".format(res))

    res = erlangcp.get_average_number_customers_in_system(lambda_=lambda_, mu=mu, nu=nu, number_agents=number_agents,
                                                          size_waiting_room=size_waiting_room)
    print("Average number customers in system: {}".format(res))

    res = erlangcp.get_number_agents_for_chat(lambda_=12/3600, mu=1/180, max_waiting_time=20, nu=0.05/3,
                                              abort_prob=0.2, max_sessions=2, share_sequential_work=0.15)
    print("Number of agents for chat ".format(res))
