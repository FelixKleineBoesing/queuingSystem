import inspect

from src.controller.helpers import IntList, FloatList, check_length_list_equality, ListIntList, ListFloatList
from src.misc.helper_functions import annotation_type_checker
from src.modelling.capacity_planning.backoffice.backoffice import BackOfficeCalculator


class BackOfficeController:

    @annotation_type_checker
    @check_length_list_equality
    def get_number_agents(self, interval: IntList, volume: ListIntList, aht: ListIntList, backlog_within:
                          IntList, occupancy: FloatList, backlog_sum: IntList):

        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_number_agents).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, volume: FloatList, aht: IntList, backlog_within: int, occupancy: float,
                 backlog_sum: int):
            lambdas = [v / interval for v in volume]

            kwargs = {"lambdas": lambdas, "ahts": aht,
                      "backlog_sum": backlog_sum / interval,
                      "backlog_within": backlog_within, "occupancy": occupancy}

            backoffice = BackOfficeCalculator()
            number_agents = backoffice.get_number_agents(**kwargs)

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
    def get_volume(self, interval: IntList, number_agents: ListFloatList, aht: ListIntList,
                   backlog_within: IntList, occupancy: FloatList):
        func_args = locals()
        func_inspect = inspect.getfullargspec(self.get_volume).args
        func_inspect.remove("self")
        func_args = {key: value for key, value in func_args.items() if key in func_inspect and value is not None}

        def func(interval: int, number_agents: FloatList, aht: IntList, backlog_within: int, occupancy: float):
            kwargs = {"number_agents": number_agents, "ahts": aht, "backlog_within": backlog_within,
                      "occupancy": occupancy}

            backoffice = BackOfficeCalculator()
            volume = backoffice.get_volume(**kwargs)

            return [v * interval for v in volume]

        if isinstance(interval, int):
            return func(**func_args)
        else:
            number_agents_list = []
            for i in range(len(interval)):
                args = {key: value[i] for key, value in func_args.items()}
                number_agents_list.append(func(**args))
            return number_agents_list
