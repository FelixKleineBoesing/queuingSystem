import unittest
import datetime

from src.misc.date_conversion import convert_datetime_to_unix
from src.controller.holidays import HolidayController


class HolidayControllerTester(unittest.TestCase):

    def test_get_countries(self):
        controller = HolidayController()
        countries = controller.get_holiday_countries()
        self.assertIn("Argentina", countries)
        self.assertIn("Austria", countries)
        self.assertIn("Belgium", countries)
        self.assertIn("Germany", countries)
        self.assertIn("Norway", countries)
        self.assertIn("Portugal", countries)
        self.assertIn("Romania", countries)
        self.assertIn("Turkey", countries)
        self.assertIn("Ukraine", countries)

    def test_get_provinces(self):
        controller = HolidayController()
        provinces = controller.get_provinces_of_country("Germany")
        self.assertIn("BW", provinces)
        self.assertIn("BB", provinces)
        self.assertIn("SL", provinces)
        self.assertIn("TH", provinces)
        self.assertIn("HE", provinces)

    def test_get_working_days_per_week(self):
        controller = HolidayController()
        start_date = convert_datetime_to_unix([datetime.datetime(year=2019, month=12, day=30)])[0]
        end_date = convert_datetime_to_unix([datetime.datetime(year=2021, month=1, day=11)])[0]
        country = "Germany"
        province = None
        compensation_method = "month"
        compensation_interval = None
        comp_working_days = controller.get_working_days_per_week(date_start=start_date, date_end=end_date,
                                                                 country=country, province=province,
                                                                 compensation_method=compensation_method,
                                                                 compensation_interval=compensation_interval)


