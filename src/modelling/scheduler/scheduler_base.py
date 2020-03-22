import logging
import abc


class Scheduler(abc.ABC):

    def __init__(self, number_agents_per_half_hour: list, lunch_time: int = 1,
                 number_intervals_per_agent: int = 17, lunch_time_border: int = 6, verbose: bool = True):
        self.number_intervals_per_agent = number_intervals_per_agent
        self.lunch_time = lunch_time
        self.lunch_time_border = lunch_time_border
        self.number_agents_per_half_hour = number_agents_per_half_hour
        self.verbose = verbose

    @abc.abstractmethod
    def solve(self):
        pass

    def log(self, message: str, level: str = "info"):
        """
        if the scheduler attribute verbose is set to true it will log with the defined logging level

        :param message: message that should be logged
        :param level: default level is info. The levels are possible that are attributes of the logging package
        :return:
        """
        if hasattr(logging, level):
            logging_func = getattr(logging, level)
        else:
            raise ValueError("Wrong logging level!")
        if self.verbose:
            logging_func(message)
