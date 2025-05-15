from decimal import Decimal


def value_adjustment(percent, value, mirrored=False):
    if percent == 0:
        return 0

    part_value = value * Decimal(str(percent / 100))
    if mirrored:
        part_value = -part_value

    return part_value
