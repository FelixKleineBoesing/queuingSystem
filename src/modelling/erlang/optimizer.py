import copy
import inspect
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
        assert isinstance(method, MethodType), "the parameter method must be of type MethodType. Therefore it must " \
                                               "be a method of some class!"
        assert isinstance(kwargs, dict), "kwargs must be of type dictionary"
        assert isinstance(optim_argument, str), "optim_argument must be of type str"
        assert isinstance(target_value, (float, int)), "target value must be integer or float"
        func_inspect = inspect.getfullargspec(method)
        args = func_inspect.args
        annotations = func_inspect.annotations
        assert optim_argument in args, "The optim_argument '{}' is not an argument of the specified function!".format(optim_argument)
        assert all([arg in args for arg in kwargs.keys()]), "One of the supplied arguments is not present inside the "
        assert all([isinstance(value, annotations[key]) for key, value in kwargs.items()]), \
            "One of the supplied arguments has the wrong return type!"
        target_type = annotations[optim_argument]
        kwargs = copy.deepcopy(kwargs)

        def optim_func(x):
            kwargs[optim_argument] = target_type(x)
            res = (target_value - method(**kwargs)) ** 2
            return res

        result = minimize_scalar(optim_func)
        return result.x

