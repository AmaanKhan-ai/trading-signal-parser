from datetime import datetime
import pytz

def get_time_cst():
    cst = pytz.timezone("US/Central")
    return datetime.now(cst).strftime("%I:%M %p CST")