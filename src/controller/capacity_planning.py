from src.modelling.capacity_planning import ErlangC, ErlangCP


class CapacityPlanningInboundPhone:

    def get_number_agents_for_service_level(self, interval: int, volume: float, aht: int, service_level: float,
                                            service_time: float, size_room: int = None,
                                            patience: int = None, retrial: float = None):
        """
        calculates the number of agents that are required to hit the specified values

        :param interval: interval in seconds, that you want to observe
        :param volume: the number of contacts in that interval
        :param aht: average handling time
        :param service_level: level of service (percentage of satisfied customers)
        :param service_time: time in seconds in which % percent (service time) customer call must be
        :param size_room: size of the waiting room
        :param patience: average patience in seconds
        :param retrial: how many percent of the people dial
        :return:
        """
        kwargs = {}
        kwargs["lambda_"] = volume / interval
        kwargs["mu"] = 1 / aht
        max_waiting_target = 1 - service_level

        if patience is not None or size_room is not None or retrial is not None:
            assert patience is not None, "patience has to be not none when size room is selected"
            erlang = ErlangCP()
            kwargs["nu"] = 1 /patience
            kwargs["size_room"] = size_room
            kwargs["retrial"] = retrial
        else:
            erlang = ErlangC()
        number_agents = erlang.minimize(erlang.get_max_waiting_probability, kwargs=kwargs,
                                        optim_argument="number_agents", target_value=max_waiting_target)

        return number_agents

    def get_volume_for_service_level(self, interval: int, number_agents: int, aht: int, service_level: float,
                                     service_time: float, size_room: int, patience: int, retrial: float):
        """
        calculates the volume that are that the given agents are able to handle with the specified arguments

        :param interval: interval in seconds, that you want to observe
        :param number_agents: the number of agents that are used in this interval
        :param aht: average handling time
        :param service_level: level of service (percentage of satisfied customers)
        :param service_time: time in seconds in which % percent (service time) customer call must be
        :param size_room: size of the waiting room
        :param patience: average patience in seconds
        :param retrial: how many percent of the people dial
        :return:
        """
        kwargs = {}
        kwargs["number_agents"] = number_agents
        kwargs["mu"] = 1 / aht
        max_waiting_target = 1 - service_level

        if patience is not None or size_room is not None or retrial is not None:
            assert patience is not None, "patience has to be not none when size room is selected"
            erlang = ErlangCP()
            kwargs["nu"] = 1 /patience
            kwargs["size_room"] = size_room
            kwargs["retrial"] = retrial
        else:
            erlang = ErlangC()
        lambda_ = erlang.minimize(erlang.get_max_waiting_probability, kwargs=kwargs,
                                  optim_argument="lambda_", target_value=max_waiting_target)

        return lambda_ * interval

    def get_number_agents_for_average_waiting_time(self, interval: int, volume: float, aht: int, asa: int,
                                                   abandonment: float, size_room: int, patience: int, retrial: float):
        """
        calculates the number of agents that are required to hit the specified waiting time

        :param interval: interval in seconds, that you want to observe
        :param volume: the number of agents that are used in this interval
        :param aht: average handling time
        :param asa: average waiting time
        :param abandonment: percentage of caller that abandon
        :param size_room: size of the waiting room
        :param patience: average patience in seconds
        :param retrial: how many percent of the people dial
        :return:
        """
        pass

    def get_average_waiting_time_for_number_agents(self, interval: int, number_agents: float, aht: int, asa: int,
                                                   abandonment: float, size_room: int, patience: int, retrial: float):
        """
        calculates the volume that the

        :param interval: interval in seconds, that you want to observe
        :param number_agents: the number of agents that are used in this interval
        :param aht: average handling time
        :param asa: average waitinasg time
        :param abandonment: percentage of caller that abandon
        :param size_room: size of the waiting room
        :param patience: average patience in seconds
        :param retrial: how many percent of the people dial
        :return:
        """
        pass