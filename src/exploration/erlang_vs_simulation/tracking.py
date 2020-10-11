import mlflow
import numpy as np
from src.exploration.erlang_vs_simulation.helpers import compare_number_agents, compare_lambda, compare_aht, \
    get_service_levels_pre_allocated

NUMBERS_AGENTS = (1, 1000)
LAMBDAS = (1, 500)
AHTS = (1, 1000)


def run_calculations(size: int = 100, aht_sd_rel: float = 0.1):
    number_agents = int((np.random.random(size=size) * (NUMBERS_AGENTS[1] - NUMBERS_AGENTS[0])) + NUMBERS_AGENTS[0])
    lambdas = (np.random.random(size=size) * (LAMBDAS[1] - LAMBDAS[0])) + LAMBDAS[0]
    ahts = (np.random.random(size=size) * (AHTS[1] - AHTS[0])) + AHTS[0]

    get_service_levels_pre_allocated(number_agents=number_agents, ahts=ahts, lambdas=lambdas, aht_sd_rel=aht_sd_rel,
                                     max_waiting_time=20)

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:4040")
    mlflow.set_experiment("/Erlang-vs-Simulation")
    run_calculations()