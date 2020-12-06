from typing import Tuple
import holidays
import pandas as pd

from src.controller.internal_helpers import IntList, FloatList, check_length_list_equality, ListIntList, ListFloatList, \
    get_possible_countries_from_library
from src.misc.date_calculation import construct_datetime_list
from src.misc.helper_functions import annotation_type_checker
from src.misc.date_conversion import convert_unix_to_datetime, convert_datetime_to_isoweek, \
    convert_isoweek_to_datetime, get_months_from_datetime, get_year_from_datetime

COUNTRIES, PROVINCES = get_possible_countries_from_library()


class HolidayController:

    @annotation_type_checker
    def get_working_days_per_week(self, date_start: int, date_end: int, country: str, province: str = None,
                                  compensation_method: str = "month", compensation_interval: Tuple = None):
        assert compensation_method in ["month", "week_interval"], "Compensation method '{}' is not valid!".\
            format(compensation_method)
        if compensation_interval is not None:
            assert compensation_method is "month"
        country_holidays = getattr(holidays, country)
        if province is not None:
            country_holidays = getattr(country_holidays, province)
        country_holidays = country_holidays()
        date_start = convert_unix_to_datetime(date_start)
        date_end = convert_unix_to_datetime(date_end)
        date_list = construct_datetime_list(date_start, date_end, {"days": 1})
        holiday = [1 if d in country_holidays else 0 for d in date_list]
        isoweeks = convert_datetime_to_isoweek(date_list)

        data = pd.DataFrame({"dates": date_list, "CW": isoweeks, "holiday": holiday})
        number_working_days = data.groupby("CW", as_index=False).sum()
        number_working_days["working_days"] = 5 - number_working_days["holiday"]
        if compensation_method is "month":
            dates = convert_isoweek_to_datetime(number_working_days["CW"])
            months = get_months_from_datetime(dates)
            years = get_year_from_datetime(dates)
            number_working_days["year_month"] = ["{}-{}".format(y, m) for y, m in zip(years, months)]
            monthly_working_days = number_working_days.groupby("year_month", as_index=False)["working_days"].\
                agg(("sum", "count"))
            monthly_working_days.reset_index(inplace=True)
            monthly_working_days["compensated_working_days"] = \
                monthly_working_days["sum"] / monthly_working_days["count"]
            monthly_working_days.drop(["sum", "count"], axis=1, inplace=True)
            number_working_days = pd.merge(number_working_days, monthly_working_days, how="left", on="year_month")
            number_working_days.drop(["holiday", "year_month"], axis=1, inplace=True)
        else:
            pass

        return number_working_days

    @staticmethod
    def get_holiday_countries():
        return COUNTRIES

    @staticmethod
    def get_provinces_of_country(country: str):
        assert country in PROVINCES, "Country '{}' is not in available COUNTRIES".format(country)
        return PROVINCES[country]

