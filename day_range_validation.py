from datetime import datetime, timezone, timedelta

def is_valid_day_range(days_range):
    valid_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    current_day_index = datetime.now(timezone(timedelta(hours=5, minutes=30))).weekday()
    current_day = valid_days[current_day_index]
    start_day, end_day = days_range.split('-')
    
    # Get the indices of the start and end days
    start_index = valid_days.index(start_day)
    end_index = valid_days.index(end_day)
    
    # Adjust end index if it's before the start index to handle wrapping over the week
    if end_index < start_index:
        end_index += 7
    
    # Check if the current day index is within the valid range
    return start_index <= current_day_index <= end_index