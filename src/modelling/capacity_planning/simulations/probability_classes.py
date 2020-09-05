import numpy as np
import abc

from scipy.stats import poisson
from sklearn.neighbors import KernelDensity as KD


class Probability(abc.ABC):

    @abc.abstractmethod
    def draw(self):
        pass


class ListDrawer(Probability):

    def __init__(self, data: list):
        self.data = data

    def draw(self, size=1):
        return np.random.choice(self.data)


class KernelDensity(Probability):

    def __init__(self, data: list):
        self.model = KD(kernel="gaussian")
        self.model.fit(data)

    def draw(self, size=1):
        self.model.sample(n_samples=size)


class ErlangDistribution(Probability):

    def __init__(self, lambda_: float):
        self.lambda_ = lambda_
        self.poisson = poisson(lambda_)

    def draw(self, size=1):
        return self.poisson.rvs(size=size)
