import logging
import abc


class Scheduler(abc.ABC):

    def __init__(self, demands: list, lunch_time: int = 1,
                 number_intervals_per_agent: int = 17, lunch_time_border: int = 6, verbose: bool = True):
        assert isinstance(demands, list)
        assert isinstance(lunch_time, int)
        assert isinstance(number_intervals_per_agent, int)
        assert isinstance(lunch_time_border, int)
        assert isinstance(verbose, bool)
        assert number_intervals_per_agent <= len(demands), "number_intervals_per_agent must be smaller or equal to " \
                                                           "the length of the demands list."
        assert lunch_time_border * 2 + lunch_time <= number_intervals_per_agent, "the lunch_time_border x 2 + lunch_" \
                                                                                 "time has to be smaller or equal " \
                                                                                 "to the number_intervals_per_agent"

        self.number_intervals_per_agent = number_intervals_per_agent
        self.lunch_time = lunch_time
        self.lunch_time_border = lunch_time_border
        self.number_agents_per_half_hour = demands
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
