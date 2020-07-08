import inspect
from typing import Union, List

from src.controller.helpers import IntList, FloatList, check_length_list_equality, ListIntList, ListFloatList
from src.misc.helper_functions import annotation_type_checker


class BackOfficeController:

    @annotation_type_checker
    @check_length_list_equality
    def get_number_agents(self, interval: IntList, incoming_value: ListIntList, aht: ListIntList, backlog_within_hours:
                          IntList, occupancy: FloatList):
        pass

    @annotation_type_checker
    @check_length_list_equality
    def get_volume(self, interval: IntList, availabe_agents: ListFloatList, aht: ListIntList,
                   backlog_within_hours: IntList, occupancy: FloatList):
        pass
