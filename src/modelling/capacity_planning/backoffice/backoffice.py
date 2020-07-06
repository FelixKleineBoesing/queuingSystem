import numpy as np


class BackOfficeCalculator:

    def get_required_agents(self, lambdas: list, ahts: list, open_index: int, closed_index: int,
                            backlog_within: int, occupancy: float):
        """
        calculates the necessary agents per timestep if timestep is one second.

        :param lambdas: the volumes but divided by interval. So its volume per second
        :param ahts:
        :param open_index:
        :param closed_index:
        :param backlog_within:
        :param occupancy:
        :return:
        """
        assert closed_index < len(lambdas)
        assert open_index < len(lambdas)
        assert open_index < closed_index
        assert closed_index - open_index + 1 == len(ahts), "mus must be as long as the interval from open to closed"
        assert backlog_within < len(ahts)
        assert 0 < occupancy <= 1
        backlog_sum = np.sum(lambdas[:open_index])
        open_volumes = np.array(lambdas[open_index:(closed_index + 1)])
        backlog_prioritized = np.zeros((len(open_volumes), ))
        backlog_prioritized[:backlog_within + 1] = backlog_sum / backlog_within
        volumes_sum = open_volumes + backlog_prioritized
        required_agents = (volumes_sum * np.array(ahts)) / occupancy
        return required_agents.tolist()

    def get_possible_volume(self, available_agents: list, ahts: list, open_index: int, closed_index: int,
                            backlog_within: int, occupancy: float):
        assert closed_index < len(available_agents)
        assert open_index < len(available_agents)
        assert open_index < closed_index
        assert closed_index - open_index + 1 == len(ahts), "mus must be as long as the interval from open to closed"
        assert backlog_within < len(ahts)
        assert 0 < occupancy <= 1
        return (np.array(available_agents) / (np.array(ahts))).tolist()




