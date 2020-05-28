import copy
import inspect
import numpy as np
import plotly.graph_objs as go
from types import MethodType, FunctionType
from typing import Union

from pulp import LpProblem, LpMinimize, LpVariable
from scipy.optimize import minimize_scalar


class Optimizer:
    """
    The Optimizer is a helper class that can be inherited to any class to make any method of the origin class
    optimizable in terms of finding a fitting value for the missing argument.
    Therefore all arguments need a type annotation.
    """
    def __init__(self):
        """

        """
        self.argument_bounds = {}

    def get_bounds(self, arg):
        pass

    def minimize(self, method: Union[MethodType, FunctionType], kwargs: dict, optim_argument: str,
                 target_value: Union[float, int]):
        """
        minimizes the squared error of any given method with given parameters and one optim_argument which
        should be estimated

        :param method: the method that should be evaluated
        :param kwargs: the fixed parameters
        :param optim_argument: the parameter that should be estimated
        :param target_value: the value of the method that should be the result
        :return:
        """
        assert isinstance(method, (MethodType, FunctionType)), "the parameter method must be of type " \
                                                               "MethodType or FunctionType. Therefore it must " \
                                                               "be a method of some class!"
        assert isinstance(kwargs, dict), "kwargs must be of type dictionary"
        assert isinstance(optim_argument, str), "optim_argument must be of type str"
        assert isinstance(target_value, (float, int)), "target value must be integer or float"

        # TODO find a way to get brackets for optimizing / user other minimize method
        optim_func, target_type = self.get_optim_func(method=method, kwargs=kwargs, optim_argument=optim_argument,
                                                      target_value=target_value)

        result = minimize_scalar(optim_func)
        return target_type(result.x)

    def get_optim_func(self, method: Union[MethodType, FunctionType], kwargs: dict, optim_argument: str,
                       target_value: Union[float, int]):

        func_inspect = inspect.getfullargspec(method)
        args = func_inspect.args
        annotations = func_inspect.annotations
        assert optim_argument in args, "The optim_argument '{}' is not an argument of the specified function!". \
            format(optim_argument, method)
        for arg in kwargs.keys():
            assert arg in args, "The supplied argument {} is no argument of function {}!".format(arg, str(method))
        for key, value in kwargs.items():
            assert isinstance(value, annotations[key]), "The supplied value for {} is of type {} and not of type {}". \
                format(key, type(value), annotations[key])

        target_type = annotations[optim_argument]
        kwargs = copy.deepcopy(kwargs)

        def optim_func(x):
            kwargs[optim_argument] = target_type(x)
            try:
                return (target_value - method(**kwargs)) ** 2
            except AssertionError:
                return np.Inf
            except Exception as e:
                print(e)
        return optim_func, target_type

    def plot_cost_function(self, method: Union[MethodType, FunctionType], kwargs: dict, optim_argument: str,
                 target_value: Union[float, int], boundaries: tuple, steps: int = 100):
        """
        plots the cost function with the change of the optim arguments

        :param method:
        :param kwargs:
        :param optim_argument:
        :param target_value:
        :return:
        """
        optim_func, target_type = self.get_optim_func(method=method, kwargs=kwargs, optim_argument=optim_argument,
                                                      target_value=target_value)
        results = []
        input_values = []
        step = (boundaries[1] - boundaries[0]) / steps
        for i in range(steps):
            x = boundaries[0] + step * i
            res = optim_func(x)
            results.append(res)
            input_values.append(x)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=input_values, y=results, name="Loss Values", line={"width": 10, "color": "black"}))
        return fig
