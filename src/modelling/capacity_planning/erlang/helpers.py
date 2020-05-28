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
        if self._lower_bound is None:
            return np.Inf
        else:
            return self._lower_bound

    @property
    def start(self):
        if self._start is None:
            return 0
        else:
            return self._start