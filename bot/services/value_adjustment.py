from decimal import Decimal


def value_adjustment(percent, value, mirrored=False):
    if percent == 0:
        return value

    part_value = value * Decimal(str(percent / 100))
    if mirrored:
        part_value = -part_value

    return value + part_value
