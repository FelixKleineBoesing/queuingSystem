import numpy as np
import abc

from scipy.stats import poisson, expon, exponweib, norm
from sklearn.neighbors import KernelDensity as KD


class Probability(abc.ABC):

    @abc.abstractmethod
    def _draw(self, size: int = 1):
        pass

    def draw(self, size: int = 1):
        values = self._draw(size=size)
        values[values < 0] = 0
        return values


class ListDrawer(Probability):

    def __init__(self, data: list):
        self.data = data

    def _draw(self, size: int = 1):
        return np.random.choice(self.data, size=size)


class KernelDensity(Probability):

    def __init__(self, data: list):
        self.model = KD(kernel="gaussian")
        self.model.fit(data)

    def _draw(self, size: int = 1):
        self.model.sample(n_samples=size)


class ErlangDistribution(Probability):

    def __init__(self, lambda_: float):
        self.lambda_ = lambda_
        self.poisson = poisson(lambda_)

    def _draw(self, size: int = 1):
        return self.poisson.rvs(size=size)


class ExponentialDistribution(Probability):

    def __init__(self, x: float):
        self.x = x
        self.exp = expon(x)

    def _draw(self, size: int = 1):
        return self.exp.rvs(size=size)


class WeibullDistribution(Probability):

    def __init__(self, x: float):
        self.x = x
        self.weib = exponweib(x)

    def _draw(self, size: int = 1):
        return self.weib.rvs(size=size)


class NormalDistribution(Probability):

    def __init__(self, mean: float, sd: float):
        self.mean = mean
        self.sd = sd
        self.normal_dist = norm(loc=self.mean, scale=self.sd)

    def _draw(self, size: int = 1):
        return self.normal_dist.rvs(size=size)