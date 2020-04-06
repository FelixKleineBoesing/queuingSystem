import copy
from types import MethodType
from typing import Union
from scipy.optimize import minimize_scalar


class Optimizer:

    def __init__(self):
        pass

    def minimize(self, method: MethodType, kwargs: dict, optim_argument: str, target_value: Union[float, int]):
        """
        minimizes the squared error of any given method with given parameters and one optim_argument which
        should be estimated

        :param method: the method that should be evaluated
        :param kwargs: the fixed parameters
        :param optim_argument: the parameter that should be estimated
        :param target_value: the value of the method that should be the result
        :return:
        """

        kwargs = copy.copy(kwargs)

        def optim_func(x):
            kwargs[optim_argument] = x
            res = (target_value - method(**kwargs)) ** 2
            return res

        result = minimize_scalar(optim_func)
        return result.x

