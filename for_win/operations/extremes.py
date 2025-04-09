from decimal import Decimal


def find_extremes(df):
    swings = []
    batch = 0
    direction = None

    def add_swing(swing_type, level, open_price, close_price, count, start, end):
        swings.append(
            {
                "type": swing_type,
                "level": level,
                "open": open_price,
                "close": close_price,
                "count_candles": count,
                "time_start": start,
                "time_end": end,
            }
        )

    for i, row in enumerate(df.itertuples(index=False)):
        open_price = Decimal(str(row.open))
        close_price = Decimal(str(row.close))
        high = Decimal(str(row.high))
        low = Decimal(str(row.low))

        is_up = open_price < close_price
        is_last = i == len(df) - 2

        if is_up:  # UP
            if direction == "UP":  # Stay direction
                batch += 1
                if is_last:
                    add_swing(
                        "UP",
                        high,
                        Decimal(str(df.iloc[i - batch].open)),
                        close_price,
                        batch,
                        df.iloc[i - batch].time,
                        row.time,
                    )
            elif direction == "DOWN":  # Change direction
                levels = [Decimal(str(df.iloc[i - 1].low)), low]
                if batch >= 2:
                    levels.append(Decimal(str(df.iloc[i - 2].low)))
                else:
                    if i + 1 < len(df) and Decimal(str(df.iloc[i + 1].open)) < Decimal(
                        str(df.iloc[i + 1].close)
                    ):
                        levels.append(Decimal(str(df.iloc[i + 1].low)))

                add_swing(
                    "DOWN",
                    min(levels),
                    Decimal(str(df.iloc[i - batch].open)),
                    Decimal(str(df.iloc[i - 1].close)),
                    batch,
                    df.iloc[i - batch].time,
                    df.iloc[i - 1].time,
                )

                direction, batch = "UP", 1
            else:  # Start
                direction, batch = "UP", 1

        else:  # DOWN
            if direction == "DOWN":  # Stay direction
                batch += 1
                if is_last:
                    add_swing(
                        "DOWN",
                        low,
                        Decimal(str(df.iloc[i - batch].open)),
                        close_price,
                        batch,
                        df.iloc[i - batch].time,
                        row.time,
                    )
            elif direction == "UP":  # Change direction
                levels = [Decimal(str(df.iloc[i - 1].high)), high]
                if batch >= 2:
                    levels.append(Decimal(str(df.iloc[i - 2].high)))
                else:
                    if i + 1 < len(df) and Decimal(str(df.iloc[i + 1].open)) > Decimal(
                        str(df.iloc[i + 1].close)
                    ):
                        levels.append(Decimal(str(df.iloc[i + 1].high)))

                add_swing(
                    "UP",
                    max(levels),
                    Decimal(str(df.iloc[i - batch].open)),
                    Decimal(str(df.iloc[i - 1].close)),
                    batch,
                    df.iloc[i - batch].time,
                    df.iloc[i - 1].time,
                )

                direction, batch = "DOWN", 1
            else:  # Start
                direction, batch = "DOWN", 1

    return swings
