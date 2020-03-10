from ortools.sat.python import cp_model


class GORScheduler:

    def __init__(self, number_agents: int):
        self.model = cp_model.CpModel()
        self.number_agents = number_agents
