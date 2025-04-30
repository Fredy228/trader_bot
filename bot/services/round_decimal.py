from decimal import Decimal, ROUND_HALF_UP


def round_decimal(value, level="0.01"):
    return value.quantize(Decimal(level), rounding=ROUND_HALF_UP)
