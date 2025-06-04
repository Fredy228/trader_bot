from decimal import Decimal
import pandas as pd

from services.logger import logger
from operations.extremes import check_patterns
from operations.trade_by_history_trend import trade_by_history_trend
from operations.check_orders_test import check_orders, get_orders

from config import DEBUG_MODE


def trade_test_1(df):
    direction = None
    level_up = None
    prev_idx_up = 0
    level_down = None
    prev_idx_down = 0
    trend = pd.DataFrame(columns=["time", "trend"])
    len_df = len(df)

    for i, row in enumerate(df.itertuples(index=False)):

        percent = (i / len_df) * 100
        filled_length = int(50 * i // len_df)
        bar = "#" * filled_length + "-" * (50 - filled_length)
        print(f"\r[{bar}] {percent:.1f}%", end="", flush=True)

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

        if i < len(df) - 2:
            check_orders(
                time,
                df.iloc[i + 1]["time"],
                {
                    "open": open_price,
                    "close": close_price,
                    "high": high,
                    "low": low,
                    "time": time,
                },
            )

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

            if DEBUG_MODE == 1:
                logger.info(
                    f"Pattern high: {df.iloc[idx_up_value]['high']} {df.iloc[idx_up_value]['time']}"
                )

            if level_up is None or max_value > Decimal(str(level_up["level"])):
                if level_up is not None:
                    prev_idx_up = level_up["idx"]
                new_candle = df.iloc[idx_up_value]
                level_up = {"level": max_value, "idx": idx_up_value}
                trend.loc[len(trend)] = [
                    new_candle["time"],
                    float(max_value),
                ]

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

            if DEBUG_MODE == 1:
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
                trend.loc[len(trend)] = [
                    new_candle["time"],
                    float(min_value),
                ]

                return True
            else:
                return False

        if not is_up:
            is_broken_up = update_up_level(i - 2, i)

            if is_broken_up:
                if direction == "DOWN":
                    is_change_trend = True
                    logger.info(f"Зміна тренду на UP {time}")
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
                    logger.info(f"Зміна тренду на DOWN {time}")
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

        trade_by_history_trend(
            Decimal(level_up["level"]), Decimal(level_down["level"]), direction, time
        )

    markers = get_orders()

    return trend, markers
