from datetime import datetime
from time import mktime


def published_parsed_to_datetime(published_parsed):
    """
    Converts a time.struct_time object into a datetime.datetime object
    (Feedparser gives published times in time.struct_time)

    :param published_parsed: (time.struct_time)
    :return: (datetime.datetime)
    """
    # print published_parsed, datetime.fromtimestamp(mktime(published_parsed))
    return datetime.fromtimestamp(mktime(published_parsed))