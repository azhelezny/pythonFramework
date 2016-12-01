import datetime
import time


def get_unix_timestamp():
    return long(time.time())


def get_date_as_string(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return str(date).replace(":", "-")
