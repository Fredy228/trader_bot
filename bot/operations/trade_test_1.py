from decimal import Decimal

from services.logger import logger
from operations.candles import get_direction_candle
from operations.extremes import check_patterns


def trade_test_1(df):
    direction = None
    level_up = None
    prev_idx_up = 0
    level_down = None
    prev_idx_down = 0

    for i, row in enumerate(df.itertuples(index=False)):
        print(f"i: {i}")

        if i < 2:
            continue

        open_price = Decimal(str(row.open))
        close_price = Decimal(str(row.close))
        high = Decimal(str(row.high))
        low = Decimal(str(row.low))
        time = row.time

        is_up = open_price < close_price
        is_change_trend = False

        prev_row = df.iloc[i - 1]
        prev_prev_row = df.iloc[i - 2]

        # Check patterns
        if not check_patterns(prev_prev_row, prev_row, row):
            continue

        # Check change trend
        def update_up_level(from_idx, to_idx):
            print(f"from_idx: {from_idx}, to_idx: {to_idx}")
            nonlocal level_up, prev_idx_up
            idx_up_broken = None
            for j in range(from_idx, to_idx + 1):
                if level_up is None or df.iloc[j].high > level_up["level"]:
                    idx_up_broken = j

            if idx_up_broken is not None:
                if level_up is not None:
                    prev_idx_up = level_up["idx"]
                level_up = {"level": df.iloc[idx_up_broken].high, "idx": idx_up_broken}
                return True
            return False

        def update_down_level(from_idx, to_idx):
            print(f"from_idx: {from_idx}, to_idx: {to_idx}")
            nonlocal level_down, prev_idx_down
            idx_down_broken = None
            for j in range(from_idx, to_idx + 1):
                if level_down is None or df.iloc[j].low > level_down["level"]:
                    idx_down_broken = j

            if idx_down_broken is not None:
                if level_down is not None:
                    prev_idx_down = level_down["idx"]
                level_down = {
                    "level": df.iloc[idx_down_broken].low,
                    "idx": idx_down_broken,
                }
                return True
            return False

        if not is_up:
            is_broken_up = update_up_level(i - 2, i)

            if is_broken_up:
                print("Broken ======", is_broken_up)
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
                print("Broken ======", is_broken_down)
                if direction == "UP":
                    is_change_trend = True
                    print(f"Зміна тренду DOWN {time}")
                    logger.info(f"Зміна тренду DOWN {time}")
                direction = "DOWN"

                up_new_level = None
                idx_up_level = 0
                for l in range(prev_idx_down, level_down["idx"] + 1):
                    high = df.iloc[l].high
                    if up_new_level is None or high > idx_up_level:
                        idx_up_level = l
                        up_new_level = high
                level_up = {
                    "level": up_new_level,
                    "idx": idx_up_level,
                }

        print(f"level_up: {level_up}, level_down: {level_down}")

        if level_down is None or level_up is None:
            continue

        if not is_change_trend:
            continue
