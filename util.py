""" Utility functions """
from datetime import datetime


def get_current_timestamp():
    """Get the current UNIX timestamp, location specific"""
    current_time = datetime.now()
    return int(datetime.timestamp(current_time))


def transform_timestamp(timestamp):
    """Transforms the UNIX timestamp into a readable date format as string"""
    date_time = datetime.fromtimestamp(int(timestamp))
    time_formatted = date_time.strftime('%Y-%b-%d (%H:%M:%S)')
    return time_formatted


def create_id(dict):
    array = []
    counter = 1
    for i in dict:
        array.append(int(i['id']))
    while True:
        if counter in array:
            counter += 1
        else:
            return counter