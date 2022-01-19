import time
from datetime import datetime

def get_timestamp():
    return int(1e6 * time.time())

# 1642523749895104

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)

def format_microsecond_timestamp(timestamp):
    return format_timestamp(int(str(timestamp)[:10]))

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

