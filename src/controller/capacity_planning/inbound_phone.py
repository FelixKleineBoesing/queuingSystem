import inspect
from typing import Union, List

from src.controller.helpers import IntList, FloatList, check_length_list_equality
from src.misc.helper_functions import annotation_type_checker
from src.modelling.capacity_planning.erlang.erlangc import ErlangC
from src.modelling.capacity_planning.erlang.erlanga import ErlangA


class InboundPhoneController:

    @annotation_type_checker
    @check_length_list_equality
    def get_number_agents_for_service_level(self, interval: IntList, volume: FloatList, aht: IntList,
                                            service_level: FloatList, service_time: FloatList,
                                            size_room: IntList = None, patience: IntList = None,
                                            retrial: FloatList = None) -> IntList:
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
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_number_agents_for_service_level).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, volume: float, aht: int, service_level: float, service_time: float,
                 size_room: int = None, patience: int = None, retrial: float = None):
            kwargs = {"lambda_": volume / interval, "mu": 1 / aht, "max_waiting_time": service_time}

            if patience is not None or size_room is not None or retrial is not None:
                assert patience is not None, "patience has to be not none when size room is selected"
                erlang = ErlangA()
                kwargs["nu"] = 1 / patience
                if size_room is not None:
                    kwargs["size_waiting_room"] = size_room
                # kwargs["retrial"] = retrial
            else:
                erlang = ErlangC()
            number_agents = erlang.minimize(erlang.get_max_waiting_probability, kwargs=kwargs,
                                            optim_argument="number_agents", target_value=service_level)

            return number_agents

        if isinstance(interval, int):
            return func(**func_args)
        else:
            number_agents_list = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                number_agents_list.append(func(**args))
            return number_agents_list

    @annotation_type_checker
    @check_length_list_equality
    def get_volume_for_service_level(self, interval: IntList, number_agents: IntList, aht: IntList,
                                     service_level: FloatList, service_time: FloatList, size_room: IntList = None,
                                     patience: IntList = None, retrial: FloatList = None):
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
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_volume_for_service_level).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, number_agents: int, aht: int, service_level: float, service_time: float,
                 size_room: int = None, patience: int = None, retrial: float = None):

            kwargs = {"number_agents": number_agents, "mu": 1 / aht, "max_waiting_time": service_time}

            if patience is not None or size_room is not None or retrial is not None:
                assert patience is not None, "patience has to be not none when size room is selected"
                erlang = ErlangA()
                kwargs["nu"] = 1 /patience
                kwargs["size_waiting_room"] = size_room
                #kwargs["retrial"] = retrial
            else:
                erlang = ErlangC()
            lambda_ = erlang.minimize(erlang.get_max_waiting_probability, kwargs=kwargs,
                                      optim_argument="lambda_", target_value=service_level)

            return lambda_ * interval

        if isinstance(interval, int):
            return func(**func_args)
        else:
            volumes = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                volumes.append(func(**args))
            return volumes

    @annotation_type_checker
    @check_length_list_equality
    def get_number_agents_for_average_waiting_time(self, interval: IntList, volume: FloatList, aht: IntList, asa: IntList,
                                                   size_room: IntList = None, patience: IntList = None,
                                                   retrial: FloatList = None):
        """
        calculates the number of agents that are required to hit the specified waiting time

        :param interval: interval in seconds, that you want to observe
        :param volume: the number of agents that are used in this interval
        :param aht: average handling time
        :param asa: average waiting time
        :param size_room: size of the waiting room
        :param patience: average patience in seconds
        :param retrial: how many percent of the people dial

        :return:
        """
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_number_agents_for_average_waiting_time).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, volume: float, aht: int, asa: int, size_room: int = None, patience: int = None,
                 retrial: float = None):
            kwargs = {"lambda_": volume / interval, "mu": 1 / aht}

            if patience is not None or size_room is not None or retrial is not None:
                assert patience is not None, "patience has to be not none when size room is selected"
                erlang = ErlangA()
                kwargs["nu"] = 1 / patience
                kwargs["size_waiting_room"] = size_room
                #kwargs["retrial"] = retrial
            else:
                erlang = ErlangC()
            number_agents = erlang.minimize(erlang.get_average_waiting_time, kwargs=kwargs,
                                            optim_argument="number_agents", target_value=asa)

            return number_agents

        if isinstance(interval, int):
            return func(**func_args)
        else:
            number_agents_list = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                number_agents_list.append(func(**args))
            return number_agents_list

    @annotation_type_checker
    @check_length_list_equality
    def get_volume_for_average_waiting_time(self, interval: IntList, number_agents: IntList, aht: IntList,
                                            asa: IntList, size_room: IntList = None, patience: IntList = None,
                                            retrial: FloatList = None):
        """
        calculates the volume that the

        :param interval: interval in seconds, that you want to observe
        :param number_agents: the number of agents that are used in this interval
        :param aht: average handling time
        :param asa: average waitinasg time
        :param size_room: size of the waiting room
        :param patience: average patience in seconds
        :param retrial: how many percent of the people dial
        :return:
        """
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_volume_for_average_waiting_time).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, number_agents: int, aht: int, asa: int, size_room: int = None,
                 patience: int = None, retrial: float = None):
            kwargs = {"number_agents": number_agents, "mu": 1 / aht}

            if patience is not None or size_room is not None or retrial is not None:
                assert patience is not None, "patience has to be not none when size room is selected"
                erlang = ErlangA()
                kwargs["nu"] = 1 / patience
                kwargs["size_waiting_room"] = size_room
                #kwargs["retrial"] = retrial
            else:
                erlang = ErlangC()
            lambda_ = erlang.minimize(erlang.get_average_waiting_time, kwargs=kwargs,
                                      optim_argument="lambda_", target_value=asa)

            return lambda_ * interval

        if isinstance(interval, int):
            return func(**func_args)
        else:
            volumes = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                volumes.append(func(**args))
            return volumes

