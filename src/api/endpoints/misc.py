from src.api.helpers import statuscode_endpoint_wrapper
from src.controller.holidays import HolidayController


@statuscode_endpoint_wrapper
def get_compensated_working_days_per_week(body):
    controller = HolidayController()
    res = controller.get_working_days_per_week(**body)
    return res


@statuscode_endpoint_wrapper
def get_provinces_of_country(body):
    controller = HolidayController()
    res = controller.get_provinces_of_country(**body)
    return res


@statuscode_endpoint_wrapper
def get_holiday_countries(body):
    controller = HolidayController()
    res = controller.get_holiday_countries(**body)
    return res
