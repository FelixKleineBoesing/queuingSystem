import abc
import inspect
import logging

from typing import Union

import numpy as np


class ArgumentParams:

    def __init__(self, lower_bound=None, upper_bound=None, start=None):
        self._lower_bound = lower_bound
        self._upper_bound = upper_bound
        self._start = start

    @property
    def lower_bound(self):
        if self._lower_bound is None:
            return np.Inf
        else:
            return self._lower_bound

    @property
    def upper_bound(self):
        if self._upper_bound is None:
            return np.Inf
        else:
            return self._upper_bound

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start


class OptimizerArguments(abc.ABC):

    def __init__(self):
        # This dictionary stores the Function of your class that retrieve the starting point for a parameter search
        # These function get all the other arguments of the minimize function.
        self._start_functions = {}
        # this dictionary should stores objects of the class ArgumentParams for each parameter that is used in the
        # models that should be mixed in with this class
        self.argument_params = {}

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

