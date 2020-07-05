import inspect
from typing import Union, List

from src.controller.helpers import IntList, FloatList, check_length_list_equality
from src.misc.helper_functions import annotation_type_checker


class BackOfficeController:

    @annotation_type_checker
    @check_length_list_equality
    def get_number_agents(self):
        pass

    @annotation_type_checker
    @check_length_list_equality
    def get_volume(self):
        pass
