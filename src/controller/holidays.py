from typing import Tuple

from src.controller.internal_helpers import IntList, FloatList, check_length_list_equality, ListIntList, ListFloatList
from src.misc.helper_functions import annotation_type_checker


class HolidayController:

    @annotation_type_checker
    def get_workingsdays_per_week(self, date_start: int, date_end: int, country: str, province: str = None,
                                  compensation_method: str = "month", compensation_interval: Tuple = None):
        assert compensation_method in ["month", "week_interval"]
        if compensation_interval is not None:
            assert compensation_method is "month"
        return None

    def get_holiday_countries(self):
        pass

    def get_provinces_of_country(self):
        pass

