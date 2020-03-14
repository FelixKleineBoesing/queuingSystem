import pandas as pd
from ortools.sat.python import cp_model

from src.modelling.scheduler.scheduler_base import Scheduler


class GORScheduler(Scheduler):

    def __init__(self, number_agents_per_half_hour: list, lunch_time: int = 1,
                 number_intervals_per_agent: int = 17):
        super().__init__(number_intervals_per_agent=number_intervals_per_agent,
                         number_agents_per_half_hour=number_agents_per_half_hour,
                         lunch_time=lunch_time)
        self.model = None
        self._build_model()

    def _build_model(self):
        self.model = cp_model.CpModel()

    def solve(self):
        pass



if __name__ == "__main__":
    agents_per_hour = [12, 10, 13, 12, 15, 24, 22, 33, 36, 40, 31, 29, 24, 27, 22, 24, 31, 33, 34, 31, 24, 19, 10,
                       12, 12, 7, 10, 7]
    scheduler = GORScheduler(number_agents_per_half_hour=agents_per_hour, lunch_time=1,
                             number_intervals_per_agent=17)
    scheduler.solve()
