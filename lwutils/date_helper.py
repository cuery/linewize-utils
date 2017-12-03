import calendar
from pytz import timezone
from datetime import date, timedelta, datetime
from dateutil.parser import parse


class DateHelper:

    @staticmethod
    def _find_timezone(tz):
        return timezone('Pacific/Auckland') if not tz else timezone(tz)

    @staticmethod
    def today(tz=None):
        """returns today as a date object"""
        return datetime.now(DateHelper._find_timezone(tz)).date()

    @staticmethod
    def yesterday(tz=None):
        """returns yesterday as a date object"""
        return DateHelper.today(tz) - timedelta(1)

    @staticmethod
    def week(tz=None):
        """returns one week ago as a date object"""
        return DateHelper.today(tz) - timedelta(date.today().weekday())

    @staticmethod
    def month(tz=None):
        """returns beginnig of month as a date object"""
        return DateHelper.today(tz).replace(day=1)

    @staticmethod
    def days_ago(num_days, tz=None):
        """ returns timezone aware date of num_days ago as date object"""
        return DateHelper.today(tz) - timedelta(num_days)

    @staticmethod
    def previous_day(day):
        """
            return the previous day for a given day
            e.g. 2014-09-17 -> 2014-09-16
        """
        return day - timedelta(1)

    @staticmethod
    def datetime_from_timestamp(timestamp, tz=None):
        """ returns timezone aware datetime object from given UTC timestamp """
        return datetime.fromtimestamp(timestamp, DateHelper._find_timezone(tz))

    @staticmethod
    def timestamp_from_datetime(datetime, tz=None):
        """ returns UTC timestamp from timezone unaware datetime """
        local_tz = DateHelper._find_timezone(tz)
        local_dt = local_tz.localize(datetime)
        timestamp = calendar.timegm(local_dt.utctimetuple())
        return timestamp

    @staticmethod
    def formated_time_and_day_from_timestamp(timestamp, tz=None):
        """
            returns timezone aware formated string of time and date from UTC timestamp
            e.g. '09:27 AM  Tuesday 27 May'
        """
        return datetime.fromtimestamp(timestamp, DateHelper._find_timezone(tz)).strftime("%I:%M %p  %A %d %B")

    @staticmethod
    def formated_day_from_timestamp(timestamp, tz=None):
        """
            returns timezone aware formated string of time and date from UTC timestamp
            e.g. '2015-11-04 17:18:34'
        """
        return datetime.fromtimestamp(timestamp, DateHelper._find_timezone(tz)).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def formated_date_from_timestamp(timestamp, tz=None):
        """
            returns timezone aware formated string of time and date from UTC timestamp
            e.g. '2015-11-04 17:18:34'
        """
        return datetime.fromtimestamp(timestamp, DateHelper._find_timezone(tz)).strftime("%Y-%m-%d")

    @staticmethod
    def formated_first_of_month_from_timestamp(timestamp, tz=None):
        return datetime.fromtimestamp(timestamp, DateHelper._find_timezone(tz)).replace(day=1).strftime("%Y-%m-%d")


    @staticmethod
    def formated_time_and_day_from_tz_aware_date_string(str):
        """
            expects str =  "2015-06-26 00:10:04+12:00"
            returns timezone aware formated string of time and date from UTC timestamp
            e.g. '09:27 AM  Tuesday 27 May'
        """
        date = parse(str)
        return date.strftime("%I:%M %p  %A %d %B")

    @staticmethod
    def formated_today(tz=None):
        """
            returns today as a formated string
            e.g. '2014-05-28'
        """
        return datetime.now(DateHelper._find_timezone(tz)).strftime("%Y-%m-%d")

    @staticmethod
    def formated_today_time(tz=None):
        return datetime.now(DateHelper._find_timezone(tz)).replace(hour=23, minute=59).strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def formated_six_days_ago(tz=None):
        """
            returns six days ago as a formated string
            e.g. '2014-05-22'
        """
        return (datetime.now(DateHelper._find_timezone(tz)) - timedelta(days=6)).strftime("%Y-%m-%d")

    @staticmethod
    def formated_six_days_ago_time(tz=None):
        return (datetime.now(DateHelper._find_timezone(tz)) - timedelta(days=6)).replace(hour=0, minute=0).strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def iso_week_number_for_date(date):
        """
            returns the iso week number for the given date
            e.g. '2014-09-16' -> 38
        """
        return date.isocalendar()[1]

    @staticmethod
    def iso_year_for_date(date):
        """
            returns the iso year for the given date
            e.g. '2014-09-16' -> 2014
            the iso year can differn from the gregorian year
            e.g. '2012-01-01' -> 2011
        """
        return date.isocalendar()[0]

    @staticmethod
    def iso_to_gregorian(iso_year, iso_week, iso_day):
        """
            returns gregorian date for iso tuple
            e.g. (2014, 38, 1) -> 2014-09-15
        """
        fourth_jan = date(iso_year, 1, 4)
        delta = timedelta(fourth_jan.isoweekday() - 1)
        year_start = fourth_jan - delta
        return year_start + timedelta(days=iso_day - 1, weeks=iso_week - 1)

    @staticmethod
    def date_range_for_iso_week_and_year(week, year):
        """
            returns start and end date for given iso week and year
            e.g. (38, 2014) -> 2014-09-15,  2014-09-21
        """
        start_date = DateHelper.iso_to_gregorian(year, week, 1)
        end_date = DateHelper.iso_to_gregorian(year, week, 7)
        return start_date, end_date

    @staticmethod
    def enumerate_date_range(start_date, end_date):
        ret = []
        if len(start_date) > 10:
            start_date = start_date[0:10]
        if len(end_date) > 10:
            end_date = end_date[0:10]
        ret.append(start_date)
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        while start_date_obj < end_date_obj:
            start_date_obj += timedelta(1)
            ret.append(start_date_obj.strftime("%Y-%m-%d"))
        return ret

    @staticmethod
    def string_to_datetime(date_string):
        return datetime.strptime(date_string, "%Y-%m-%d")

    @staticmethod
    def timestamp_from_utc_datetime(dt):
        return calendar.timegm(dt.timetuple())

    @staticmethod
    def parse_timeRange(trstring):
        return [int(''.join(a.split(":"))) for a in trstring.split(" - ")]

    @staticmethod
    def parse_date(datestr):
        if not datestr or len(datestr) == 0:
            return -1
        return int(datetime.date(*[int(a) for a in datestr.split("-")]).strftime("%s"))

    @staticmethod
    def parse_timestamp(ts):
        if not ts or int(ts) == -1:
            return ""
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")

    @staticmethod
    def parse_24hour(h24):
        if h24 != -1:
            h24 = str(h24)
            h24 = "0" * (4 - len(h24)) + h24
            return float(str(h24)[:-2]) + float(str(h24)[-2:]) / 60
        return -1
