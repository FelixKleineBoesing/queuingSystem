import mlflow
from mlflow import log_metric, log_param
import numpy as np
from src.exploration.erlang_vs_simulation.helpers import compare_number_agents, compare_lambda, compare_aht, \
    get_service_levels_pre_allocated

NUMBERS_AGENTS = (1, 1000)
LAMBDAS = (1, 500)
AHTS = (1, 1000)


def run_calculations(size: int = 100, aht_sd_rel: float = 0.1):
    mlflow.set_experiment("Erlang-vs-Simulation")
    number_agents = ((np.random.random(size=size) * (NUMBERS_AGENTS[1] - NUMBERS_AGENTS[0])) + NUMBERS_AGENTS[0]).\
        astype(np.int)
    lambdas = (np.random.random(size=size) * (LAMBDAS[1] - LAMBDAS[0])) + LAMBDAS[0]
    ahts = (np.random.random(size=size) * (AHTS[1] - AHTS[0])) + AHTS[0]

    values = get_service_levels_pre_allocated(number_agents=number_agents, ahts=ahts, lambdas=lambdas,
                                              aht_sd_rel=aht_sd_rel, max_waiting_time=20)
    for i in range(len(values["aht"])):
        with mlflow.start_run():
            log_param("aht", values["aht"][i])
            log_param("aht_sd", values["aht_sd"][i])
            log_metric("Erlang", values["Erlang"][i])
            log_metric("Simulation", values["Simulation"][i])
            log_param("number_agents", values["number_agents"][i])
            log_param("lambda_", values["lambda_"][i])


def run_ceteris_paribus_lambda_():
    pass


def run_ceteris_paribus_number_agents():
    pass


def run_ceteris_paribus_aht():
    pass


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://127.0.0.1:5001")
    run_calculations(size=5000)