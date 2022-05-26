def clamp(value, min_value, max_value):
    return min_value if value < min_value else max_value if value > max_value else value
