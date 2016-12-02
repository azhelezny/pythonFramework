import datetime
import time


def get_unix_timestamp():
    return long(time.time())


def get_date_as_string(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    return str(date).replace(":", "-").replace(" ","__")


def get_time_as_string(time_value):
    milliseconds = time_value * 1000
    hours = milliseconds / 3600000L
    milliseconds %= 3600000L
    minutes = milliseconds / 60000L
    milliseconds %= 60000L
    seconds = milliseconds / 1000L
    milliseconds %= 1000L
    return str(hours) + ":" + str(minutes) + ":" + str(seconds) + " and ~ " + str(milliseconds) + "ms"


def replace_in_file(file_path, replacements):
    lines = []
    with open(file_path) as infile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            lines.append(line)
    with open(file_path, "w")as outfile:
        for line in lines:
            outfile.write(line)
