def get_interval_levels(minimal_values: list, maximum_values: list):
    month_low = min(minimal_values[-30:])
    month_high = max(maximum_values[-30:])
    week_low = min(minimal_values[-7:])
    week_high = max(maximum_values[-7:])
    prev_day_low = minimal_values[-1]
    prev_day_high = maximum_values[-1]
    return month_low, month_high, week_low, week_high, prev_day_low, prev_day_high
