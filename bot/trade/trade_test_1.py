from decimal import Decimal

from services.logger import logger
from operations.extremes import check_patterns


def trade_test_1(df):
    direction = None
    level_up = None
    prev_idx_up = 0
    level_down = None
    prev_idx_down = 0
    trend = {"line": [], "time": []}

    for i, row in enumerate(df.itertuples(index=False)):

        if i < 2:
            continue

        prev_row = df.iloc[i - 1]
        prev_prev_row = df.iloc[i - 2]
        curr_row = df.iloc[i]

        open_price = Decimal(str(row.open))
        close_price = Decimal(str(row.close))
        high = Decimal(str(row.high))
        low = Decimal(str(row.low))
        time = row.time

        is_up = open_price < close_price
        is_change_trend = False

        print(f"i: {i}, is_up: {is_up}")

        # Check patterns
        if not check_patterns(prev_prev_row, prev_row, curr_row):
            continue

        # Check change trend
        def update_up_level(from_idx, to_idx):
            nonlocal level_up, prev_idx_up, trend
            idx_up_value = None
            max_value = None
            for j in range(from_idx, to_idx + 1):
                value_high = Decimal(str(df.iloc[j]["high"]))
                if max_value is None or value_high > max_value:
                    max_value = value_high
                    idx_up_value = j

            logger.info(
                f"Pattern high: {df.iloc[idx_up_value]['high']} {df.iloc[idx_up_value]['time']}"
            )

            if level_up is None or max_value > Decimal(str(level_up["level"])):
                if level_up is not None:
                    prev_idx_up = level_up["idx"]
                new_candle = df.iloc[idx_up_value]
                level_up = {"level": max_value, "idx": idx_up_value}
                trend["line"].append(max_value)
                trend["time"].append(new_candle["time"])
                return True
            else:
                return False

        def update_down_level(from_idx, to_idx):
            nonlocal level_down, prev_idx_down, trend
            idx_down_value = None
            min_value = None
            for j in range(from_idx, to_idx + 1):
                value_low = Decimal(str(df.iloc[j]["low"]))
                if min_value is None or value_low < min_value:
                    min_value = value_low
                    idx_down_value = j

            logger.info(
                f"Pattern low: {df.iloc[idx_down_value]['low']} {df.iloc[idx_down_value]['time']}"
            )

            if level_down is None or min_value < Decimal(str(level_down["level"])):
                if level_down is not None:
                    prev_idx_down = level_down["idx"]
                new_candle = df.iloc[idx_down_value]
                level_down = {
                    "level": min_value,
                    "idx": idx_down_value,
                }
                trend["line"].append(min_value)
                trend["time"].append(new_candle["time"])
                return True
            else:
                return False

        if not is_up:
            is_broken_up = update_up_level(i - 2, i)

            if is_broken_up:
                if direction == "DOWN":
                    is_change_trend = True
                    print(f"Зміна тренду UP {time}")
                    logger.info(f"Зміна тренду UP {time}")
                direction = "UP"

                down_new_level = None
                idx_down_level = 0
                for l in range(prev_idx_up, level_up["idx"] + 1):
                    low = df.iloc[l].low
                    if down_new_level is None or low < down_new_level:
                        idx_down_level = l
                        down_new_level = low
                level_down = {
                    "level": down_new_level,
                    "idx": idx_down_level,
                }

        else:
            is_broken_down = update_down_level(i - 2, i)

            if is_broken_down:
                if direction == "UP":
                    is_change_trend = True
                    print(f"Зміна тренду DOWN {time}")
                    logger.info(f"Зміна тренду DOWN {time}")
                direction = "DOWN"

                up_new_level = None
                idx_up_level = 0
                for l in range(prev_idx_down, level_down["idx"] + 1):
                    high = df.iloc[l].high
                    if up_new_level is None or high > up_new_level:
                        idx_up_level = l
                        up_new_level = high
                level_up = {
                    "level": up_new_level,
                    "idx": idx_up_level,
                }

        if level_down is None or level_up is None:
            continue

        if not is_change_trend:
            continue

    return trend
