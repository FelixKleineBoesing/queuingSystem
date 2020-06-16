import copy
import inspect
import traceback

import numpy as np
import logging
import plotly.graph_objs as go
from types import MethodType, FunctionType
from typing import Union

from scipy.optimize import minimize_scalar, minimize
from sortedcontainers import SortedDict

from src.modelling.capacity_planning.erlang.erlang_arguments_mixin import ErlangArgumentsMixin


class Optimizer(ErlangArgumentsMixin):
    """
    The Optimizer is a helper class that can be inherited to any class to make any method of the origin class
    optimizable in terms of finding a fitting value for the missing argument.
    Therefore all arguments need a type annotation.
    """
    def minimize(self, method: Union[MethodType, FunctionType], kwargs: dict, optim_argument: str,
                 target_value: Union[float, int], tolerance: float = 0.02):
        """
        minimizes the squared error of any given method with given parameters and one optim_argument which
        should be estimated

        :param method: the method that should be evaluated
        :param kwargs: the fixed parameters
        :param optim_argument: the parameter that should be estimated
        :param target_value: the value of the method that should be the result
        :param tolerance: the tolerance in percent by which the result may differ the requested value
        
        :return:
        """
        assert isinstance(method, (MethodType, FunctionType)), "the parameter method must be of type " \
                                                               "MethodType or FunctionType. Therefore it must " \
                                                               "be a method of some class!"
        assert isinstance(kwargs, dict), "kwargs must be of type dictionary"
        assert isinstance(optim_argument, str), "optim_argument must be of type str"
        assert isinstance(target_value, (float, int)), "target value must be integer or float"

        optim_func, target_type = self.get_optim_func(method=method, kwargs=kwargs, optim_argument=optim_argument,
                                                      target_value=target_value)
        argument_params_kwargs = copy.deepcopy(kwargs)
        if hasattr(method, "return_variable"):
            argument_params_kwargs[method.return_variable] = target_value

        argument_params = self.get_argument_params(optim_argument, **argument_params_kwargs)
        minimize_args = {}
        if argument_params is not None:
            minimize_args["bounds"] = (argument_params.lower_bound, argument_params.upper_bound)
            if argument_params.start is not None:
                minimize_args["bracket"] = (argument_params.start, argument_params.start + 1)
        # TODO add custom integer optim algorithm
        result = minimize(optim_func, argument_params.start, method="Nelder-Mead")
        value = target_type(result.x)
        if target_type is int:
            value += 1

        valid, difference = self.validate_result(value=value, target_value=target_value, kwargs=kwargs,
                                                 optim_argument=optim_argument, method=method, tolerance=tolerance)
        logging.debug("is the minimization valid: {}. The difference to the target is {} %".format(valid, difference))
        return value

    def validate_result(self, value, target_value, kwargs: dict, optim_argument, method, tolerance) -> (bool, float):
        """
        compares if the value is similar to the validation level
        :param value:
        :param kwargs:
        :param optim_argument:
        :param method:
        :param tolerance:

        :return: tuple of boolean and float
        """
        kwargs[optim_argument] = value
        validation = method(**kwargs)
        print(validation)
        return validation * (1 - tolerance) < target_value < validation * (1 + tolerance), (validation - value) / value

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

        if target_type is int:
            optim_func = self._get_int_optim_func(kwargs=kwargs, optim_argument=optim_argument,
                                                  target_type=target_type, target_value=target_value,
                                                  method=method)
        else:
            optim_func = self._get_float_optim_func(kwargs=kwargs, optim_argument=optim_argument,
                                                    target_type=target_type, target_value=target_value,
                                                    method=method)

        return optim_func, target_type

    def _get_int_optim_func(self, kwargs: dict, optim_argument: str, target_type: type, target_value: float, method):

        losses = SortedDict()

        def optim_func(x):
            try:
                if target_type(x) + 1 not in losses:
                    kwargs[optim_argument] = target_type(x) + 1
                    loss = (target_value - method(**kwargs)) ** 2
                    losses[kwargs[optim_argument]] = loss

                if target_type(x) - 1 not in losses:
                    kwargs[optim_argument] = target_type(x) - 1
                    loss = (target_value - method(**kwargs)) ** 2
                    losses[kwargs[optim_argument]] = loss

                kwargs[optim_argument] = target_type(x)
                if kwargs[optim_argument] not in losses:
                    loss = (target_value - method(**kwargs)) ** 2
                    losses[kwargs[optim_argument]] = loss
                else:
                    loss = losses[kwargs[optim_argument]]

                index = losses.index(kwargs[optim_argument])
                lower_key, lower_value = losses.peekitem(index - 1)
                if index + 1 < len(losses):
                    upper_key, upper_value = losses.peekitem(index + 1)
                    if abs(lower_key - kwargs[optim_argument]) < abs(upper_key - kwargs[optim_argument]):
                        x_point, y_point = lower_key, lower_value
                    else:
                        x_point, y_point = upper_key, upper_value
                else:
                    x_point, y_point = lower_key, lower_value

                loss_difference = ((loss - y_point) / abs(kwargs[optim_argument] - x_point)) * \
                                  abs(kwargs[optim_argument] - x)
                if np.isfinite(loss_difference):
                    loss = loss - loss_difference

                return loss
            except AssertionError:
                return np.Inf
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        return optim_func

    def _get_float_optim_func(self, kwargs: dict, optim_argument: str, target_type: type, target_value: float, method):

        def optim_func(x):
            kwargs[optim_argument] = target_type(x)
            try:
                loss = (target_value - method(**kwargs)) ** 2
                return loss
            except AssertionError:
                return np.Inf
            except Exception as e:
                print(traceback.format_exc())
                print(e)
        return optim_func

    def plot_cost_function(self, method: Union[MethodType, FunctionType], kwargs: dict, optim_argument: str,
                           target_value: Union[float, int], boundaries: tuple, steps: int = 100):
        """
        plots the cost function with the change of the optim arguments

        :param method:
        :param kwargs:
        :param optim_argument:
        :param target_value:
        :param boundaries:
        :param steps:
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


