from decimal import Decimal

from services.logger import logger
from operations.candles import get_direction_candle
from operations.extremes import check_patterns


def trade_test_1(df):
    direction = None
    level_up = 0
    level_down = 0

    for i, row in enumerate(df.itertuples(index=False)):
        if i < 2:
            break

        open_price = Decimal(str(row.open))
        close_price = Decimal(str(row.close))
        high = Decimal(str(row.high))
        low = Decimal(str(row.low))
        time = row.time

        is_up = open_price < close_price
        is_change_trend = False

        prev_row = df.iloc[i - 1]
        prev_prev_row = df.iloc[i - 2]

        if not check_patterns(prev_prev_row, prev_row, row):
            break

        # Check change trend
        if not is_up:
            max_price = max(high, prev_row.high, prev_prev_row.high)
            if max_price > level_up:
                if not level_up == 0:
                    if direction == "DOWN":
                        is_change_trend = True
                    direction = "UP"
                level_up = max_price
        else:
            min_price = min(low, prev_row.low, prev_prev_row.low)
            if min_price < level_down:
                if not level_down == 0:
                    if direction == "UP":
                        is_change_trend = True
                    direction = "DOWN"
                level_down = min_price

        if level_down == 0 or level_up == 0:
            break

        # Нужно обновить оба уровня сразу
