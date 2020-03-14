import abc


class Scheduler(abc.ABC):

    def __init__(self, number_agents_per_half_hour: list, lunch_time: int = 1,
                 number_intervals_per_agent: int = 17):
        self.number_intervals_per_agent = number_intervals_per_agent
        self.lunch_time = lunch_time
        self.number_agents_per_half_hour = number_agents_per_half_hour

    @abc.abstractmethod
    def solve(self):
        pass
