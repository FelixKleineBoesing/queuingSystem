from modelling.capacity_planning.optimizer_arguments import ArgumentParams


class ErlangArgumentsMixin:

    def __init__(self):
        self.argument_params = {
            "lambda_": ArgumentParams(lower_bound=0),
            "mu": ArgumentParams(lower_bound=0),
            "number_agents": ArgumentParams(lower_bound=1),
            "nu": ArgumentParams(lower_bound=0),
            "max_waiting_time": ArgumentParams(lower_bound=0),
            "size_waiting_room": ArgumentParams(lower_bound=0),
            "share_sequential_work": ArgumentParams(lower_bound=0, upper_bound=1),
            "max_sessions": ArgumentParams(lower_bound=1)
        }
        
        self._start_functions = {
            "lambda_": self.get_lambda_start,
            "mu": self.get_mu_start,
            "number_agents": self.get_number_agents_start,
            "nu": self.get_nu_start,
            "max_waiting_time": self.get_max_waiting_time_start,
            "size_waiting_room": self.get_size_waiting_room_start,
            "share_sequential_work": self.get_share_sequential_work_start,
            "max_sessions": self.get_max_sessions_start
        }

    def get_number_agents_start(self, lambda_: float, mu: float):
        """
        gets the initial starting point for the search of the optimum number agents

        :param lambda_:
        :param mu:
        :return:
        """
        return lambda_ / mu

    def get_lambda_start(self, number_agents: int, mu: float):
        """

        :param number_agents:
        :param mu:
        :return:
        """
        return number_agents * mu

    def get_mu_start(self, number_agents, lambda_):
        """

        :param number_agents:
        :param lambda_:
        :return:
        """
        return lambda_ / number_agents

    def get_nu_start(self):
        """

        :return:
        """
        return 0.1

    def get_max_waiting_time_start(self):
        """

        :return:
        """
        return 1

    def get_size_waiting_room_start(self):
        """

        :return:
        """
        return 1

    def get_share_sequential_work_start(self):
        """

        :return:
        """
        return 0.5

    def get_max_sessions_start(self):
        """

        :return:
        """
        return 1