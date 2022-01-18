import time
from datetime import datetime

def get_timestamp():
    return int(1e6 * time.time())

# 1642523749895104

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp)

def format_microsecond_timestamp(timestamp):
    return format_timestamp(int(str(timestamp)[:10]))
