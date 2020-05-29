import logging
import inspect
from typing import Union

from src.modelling.capacity_planning.erlang.helpers import ArgumentParams


class ErlangArgumentsMixin:

    def __init__(self):
        self.argument_params = {
            "lambda_": ArgumentParams(lower_bound=0),
            "mu": ArgumentParams(lower_bound=0),
            "number_agents": ArgumentParams(lower_bound=1),
            "nu": ArgumentParams(lower_bound=0),
            "max_waiting_time": ArgumentParams(lower_bound=0),
            "size_waiting_room": ArgumentParams(lower_bound=0),
            "share_sequential_work": ArgumentParams(lower_bound=0, upper_bound=1),
            "max_sessions": ArgumentParams(lower_bound=1)
        }
        self._start_functions = {
            "lambda_": self.get_lambda_start,
            "mu": self.get_mu_start,
            "number_agents": self.get_number_agents_start,
            "nu": self.get_nu_start,
            "max_waiting_time": self.get_max_waiting_time_start,
            "size_waiting_room": self.get_size_waiting_room_start,
            "share_sequential_work": self.get_share_sequential_work_start,
            "max_sessions": self.get_max_sessions_start
        }

    def get_argument_params(self, arg: str, **kwargs) -> Union[ArgumentParams, None]:
        """

        :param arg: argument for which the params should be exported
        :param kwargs:
        :return:
        """
        if arg in self.argument_params:
            argument_params = self.argument_params[arg]
            if arg in self._start_functions:
                start_function = self._start_functions[arg]
                args = inspect.getfullargspec(start_function).args
                kwargs = {key: value for key, value in kwargs.items() if key in args}
                try:
                    start = start_function(**kwargs)
                    argument_params.start = start
                except TypeError as e:
                    logging.debug("Starting value couldn´t be calculated because there is a value missing in "
                                  "the function. Supply it please. This is the message: {}".format(e))
                except Exception as e:
                    raise RuntimeError("There occurred an error in the calculation of the starting value! "
                                       "Exception: {}".format(e))
            return argument_params

    def get_number_agents_start(self, lambda_: float, mu: float):
        """
        gets the initial starting point for the search of the optimum number agents

        :param lambda_:
        :param mu:
        :return:
        """
        return lambda_ / mu

    def get_lambda_start(self, number_agents: int, mu: float):
        """

        :param number_agents:
        :param mu:
        :return:
        """
        return number_agents * mu

    def get_mu_start(self, number_agents, lambda_):
        """

        :param number_agents:
        :param lambda_:
        :return:
        """
        return lambda_ / number_agents

    def get_nu_start(self):
        """

        :return:
        """
        return 0.1

    def get_max_waiting_time_start(self):
        """

        :return:
        """
        return 1

    def get_size_waiting_room_start(self):
        """

        :return:
        """
        return 1

    def get_share_sequential_work_start(self):
        """

        :return:
        """
        return 0.5

    def get_max_sessions_start(self):
        """

        :return:
        """
        return 1