import numpy as np
from typing import Union


class BackOfficeCalculator:

    def get_number_agents(self, lambdas: list, ahts: list, backlog_sum: Union[int, float], backlog_within: int,
                          occupancy: float):
        """
        calculates the necessary agents per timestep if timestep is one second.

        :param lambdas: the volumes but divided by interval. So its volume per second
        :param ahts:
        :param backlog_sum:
        :param backlog_within:
        :param occupancy:
        :return:
        """
        assert backlog_within < len(ahts)
        assert 0 < occupancy <= 1
        open_volumes = np.array(lambdas)
        backlog_prioritized = np.zeros((len(open_volumes), ))
        backlog_prioritized[:backlog_within] = backlog_sum / backlog_within
        volumes_sum = open_volumes + backlog_prioritized
        required_agents = (volumes_sum * np.array(ahts)) / occupancy
        return required_agents.tolist()

    def get_volume(self, number_agents: list, ahts: list, backlog_within: int, occupancy: float):
        """

        :param number_agents:
        :param ahts:
        :param backlog_within:
        :param occupancy:
        :return:
        """
        assert backlog_within < len(ahts)
        assert 0 < occupancy <= 1
        return ((np.array(number_agents) * occupancy) / (np.array(ahts))).tolist()





