import abc


class OptimizerArguments(abc.ABC):

    def __init__(self):
        self.argument_params = {}

    @abc.abstractmethod
    def get_argument_params(self, optim_argument: str, **kwargs):
        pass