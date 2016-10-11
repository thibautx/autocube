from time import mktime
from datetime import datetime

def published_parsed_to_datetime(published_parsed):
    """
    Converts a time.struct_time object into a datetime.datetime object
    (Feedparser gives published times in time.struct_time)

    :param published_parsed: (time.struct_time)
    :return: (datetime.datetime)
    """
    return datetime.fromtimestamp(mktime(published_parsed))