import unittest
from lwutils.date_helper import DateHelper
from dateutils import date


class DateHelperTestCase(unittest.TestCase):

    def test_iso_week_for_date(self):
        self.assertEqual(38, DateHelper.iso_week_number_for_date(date(2014, 9, 15)))

    def test_iso_year_for_date(self):
        self.assertEqual(2011, DateHelper.iso_year_for_date(date(2012, 1, 1)))
        self.assertEqual(2013, DateHelper.iso_year_for_date(date(2013, 1, 1)))

    def test_date_range_for_iso_week_and_year(self):
        start_date, end_date = DateHelper.date_range_for_iso_week_and_year(38, 2014)
        self.assertEqual(date(2014, 9, 15), start_date)
        self.assertEqual(date(2014, 9, 21), end_date)

    def test_previous_day(self):
        start_day = date(2014, 9, 15)
        expected_previous_day = date(2014, 9, 14)
        self.assertEqual(expected_previous_day, DateHelper.previous_day(start_day))

    def test_enumerate_date_range(self):
        print DateHelper.enumerate_date_range("2012-01-02", "2012-01-20")
