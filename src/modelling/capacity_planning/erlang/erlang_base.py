import abc
from types import MethodType, FunctionType

from typing import Union

from src.modelling.capacity_planning.erlang.erlang_arguments import ErlangArguments
from src.modelling.capacity_planning.optimizer import Optimizer


class ErlangBase(abc.ABC):

    def __init__(self):
        self.optimizer = Optimizer(optimizer_arguments=ErlangArguments())

    def minimize(self, method: Union[MethodType, FunctionType], kwargs: dict, optim_argument: str,
                 target_value: Union[float, int], tolerance: float = 0.01):
        return self.optimizer.minimize(method=method, kwargs=kwargs, optim_argument=optim_argument,
                                       target_value=target_value, tolerance=tolerance)