from operations.candles import get_direction_candle


def check_patterns(first, second, last):
    first_direction = get_direction_candle(first)
    second_direction = get_direction_candle(second)

    if get_direction_candle(last) == "UP":  # UP
        if (second_direction == "DOWN" and first_direction == "DOWN") or (
            second_direction == "UP" and first_direction == "DOWN"
        ):
            return True

    else:  # DOWN
        if (second_direction == "UP" and first_direction == "UP") or (
            second_direction == "DOWN" and first_direction == "UP"
        ):
            return True

    return False
