from time import strptime, mktime, strftime
import time

import datetime

from util.lib.Util import Util


class TIME:
    @staticmethod
    def now():
        return str(TIME.time())

    @staticmethod
    def time():
        return int(time.time())

    @staticmethod
    def get_time_str(t):
        t = int(t)
        return str(strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)))

    @staticmethod
    def get_date_str():
        return str(datetime.date.today())

    @staticmethod
    def get_yestoday_date_str():
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        return yesterday

    @staticmethod
    def str_to_time(string):
        try:
            return int(mktime(strptime(str(string), '%Y-%m-%d %H:%M:%S')))
        except:
            Util.err()
            return 0

    @staticmethod
    def time_to_str(time_int):
        if time_int == 0:
            return ''
        if time_int == '':
            return ''
        try:
            time_int = int(time_int)
        except:
            time_int = int(float(time_int))

        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_int))

    @staticmethod
    def get_week():
        return time.strftime('%w', time.localtime())
