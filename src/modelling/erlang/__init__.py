from src.modelling.erlang.erlangb import ErlangB
from src.modelling.erlang.erlangc import ErlangC
from src.modelling.helpers import power_faculty

if __name__ == "__main__":
    print(power_faculty(10, 2))
    erlang = ErlangB()
    print(erlang.get_probability(9, 21, 3))

    erlang = ErlangC()
    print(erlang.get_max_waiting_probability(lambda_=0.1, mu=0.0033, number_agents=35, max_waiting_time=20))