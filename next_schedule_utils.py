"""
The get_next_event_time function calculates the timestamp of the next scheduled event based on the provided schedule hour and minute, taking into account the current time and timezone. 
This function is designed to determine the exact time at which the next event should occur according to the specified schedule.
"""
from datetime import datetime, timezone, timedelta

def get_next_event_time(schedule_hour, schedule_minute):
    current_time = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    schedule_dt = current_time.replace(hour=schedule_hour, minute=schedule_minute, second=0, microsecond=0)

    if schedule_dt.time() < current_time.time():
        schedule_dt += timedelta(days=1)

    return schedule_dt