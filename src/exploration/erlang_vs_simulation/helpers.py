import copy

from src.modelling.capacity_planning.erlang.erlangc import ErlangC
from src.modelling.capacity_planning.simulations.custom.sim_parts import Process, Worker, StatisticsContainer
from src.modelling.capacity_planning.simulations.custom.simulation import CallCenterSimulation
from src.modelling.capacity_planning.simulations.probability_classes import ErlangDistribution, ListDrawer, \
    NormalDistribution


def get_service_level_erlang(number_agents: int, lambda_, max_waiting_time, aht, aht_sd):
    erlang = ErlangC()
    return erlang.get_max_waiting_probability(lambda_=1 / lambda_, mu=1 / aht, number_agents=number_agents,
                                              max_waiting_time=max_waiting_time)


def get_service_level_simulation(number_agents: int, lambda_, max_waiting_time, aht, aht_sd):
    processes = [Process(open_from=60 * 60 * 8, close_from=22 * 60 * 60,
                         incoming_prob=ErlangDistribution(lambda_=lambda_),
                         patience_prob=ListDrawer([999999999]),
                         language="GERMAN", channel="PHONE")]

    workers = [Worker(work_begin=8 * 60 * 60, work_end=22 * 60 * 60,
                      ahts=NormalDistribution(mean=aht, sd=aht_sd),
                      channels=["CHAT", "PHONE"], languages=["GERMAN"]) for _ in range(number_agents)]

    callcenter = CallCenterSimulation(open_time=60 * 60 * 8, closed_time=60 * 60 * 22, worker=workers,
                                      processes=processes, size_waiting_room=None,
                                      stopping_criterita={"max_events": 10000})

    callcenter.run()
    stats = callcenter.statistics
    stats = StatisticsContainer(stats)
    return stats.get_service_level(max_waiting_time)


def get_service_levels_pre_allocated(number_agents: list, ahts: list, lambdas: list, aht_sd_rel: float,
                                     max_waiting_time: float):
    values = {"Erlang": [], "Simulation": [], "aht_sd": []}
    for i in range(len(number_agents)):
        params = {"number_agents": number_agents[i], "aht": ahts[i], "lambda_": lambdas[i],
                  "aht_sd": aht_sd_rel * ahts[i], "max_waiting_time": max_waiting_time}
        values["Erlang"].append(
            get_service_level_erlang(**params)
        )
        values["Simulation"].append(
            get_service_level_simulation(**params)
        )
        values["aht_sd"].append(aht_sd_rel * ahts[i])
    values["number_agents"] = number_agents
    values["aht"] = ahts
    values["lambda_"] = lambdas
    values["max_waiting_time"] = [max_waiting_time for _ in range(len(number_agents))]
    return values



def get_service_levels(default_parameters: dict, search_parameter: str, start: float, end: float, steps: int = 100,
                       param_type: type = int):
    copy.deepcopy(default_parameters)
    val_step = (end - start) / steps
    values = {search_parameter: [],
              "Erlang": [],
              "Simulation": []}
    for i in range(steps):
        default_parameters[search_parameter] = param_type(start + i * val_step)
        values["Erlang"].append(
            get_service_level_erlang(**default_parameters)
        )
        values["Simulation"].append(
            get_service_level_simulation(**default_parameters)
        )
        values[search_parameter].append(default_parameters[search_parameter])
    return values


def compare_number_agents(default_params: dict, start: float, end: float, steps: int = 50):
    plot_values = get_service_levels(default_parameters=default_params, search_parameter="number_agents",
                                     start=start, end=end, steps=steps, param_type=int)
    return plot_values


def compare_lambda(default_params: dict, start: float, end: float, steps: int = 50):
    plot_values = get_service_levels(default_parameters=default_params, search_parameter="lambda_",
                                     start=start, end=end, steps=steps, param_type=float)
    return plot_values


def compare_aht(default_params: dict, start: float, end: float, steps: int = 50):
    plot_values = get_service_levels(default_parameters=default_params, search_parameter="aht",
                                     start=start, end=end, steps=steps, param_type=float)
    return plot_values
