from decimal import Decimal


def find_extremes_copy(df):
    swings = []
    batch = 0
    direction = None

    for i in range(0, len(df) - 1):
        print(f"\n{i}")
        print(Decimal(f"{df["high"][i]}"))
        if Decimal(f"{df["open"][i]}") < Decimal(f"{df["close"][i]}"):
            # UP
            print("UP ", f"is last: {len(df) - 2 == i}")
            if direction == "UP":
                batch += 1
                if len(df) - 2 == i:  # last many candles
                    swings.append(
                        {
                            "type": "UP",
                            "level": Decimal(f"{df["high"][i]}"),
                            "open": Decimal(f"{df["open"][i - batch]}"),
                            "close": Decimal(f"{df["close"][i]}"),
                            "count_candles": batch,
                            "time_start": df["time"][i - batch],
                            "time_end": df["time"][i],
                        }
                    )
            elif direction == "DOWN":  # prev candles
                if batch >= 2:  # Pattern low 1
                    swings.append(
                        {
                            "type": "DOWN",
                            "level": min(
                                [
                                    Decimal(f"{df["low"][i - 1]}"),
                                    Decimal(f"{df["low"][i - 2]}"),
                                    Decimal(f"{df["low"][i]}"),
                                ]
                            ),
                            "open": Decimal(f"{df["open"][i - batch]}"),
                            "close": Decimal(f"{df["close"][i - 1]}"),
                            "count_candles": batch,
                            "time_start": df["time"][i - batch],
                            "time_end": df["time"][i - 1],
                        }
                    )
                else:  # Pattern low 2
                    levels = [
                        Decimal(f"{df["low"][i - 1]}"),
                        Decimal(f"{df["low"][i]}"),
                    ]
                    if df["low"][i + 1] and Decimal(f"{df["open"][i + 1]}") < Decimal(
                        f"{df["close"][i + 1]}"
                    ):
                        levels.append(Decimal(f"{df["low"][i + 1]}"))
                    swings.append(
                        {
                            "type": "DOWN",
                            "level": min(levels),
                            "open": Decimal(f"{df["open"][i - batch]}"),
                            "close": Decimal(f"{df["close"][i - 1]}"),
                            "count_candles": batch,
                            "time_start": df["time"][i - batch],
                            "time_end": df["time"][i - 1],
                        }
                    )
                direction = "UP"
                batch = 1

            else:  # If it is first element
                direction = "UP"
                batch = 1

        else:
            # DOWN
            print("DOWN ", f"is last: {len(df) - 2 == i}")
            if direction == "DOWN":
                batch += 1
                if len(df) - 2 == i:  # last many candles
                    swings.append(
                        {
                            "type": "DOWN",
                            "level": Decimal(f"{df["low"][i]}"),
                            "open": Decimal(f"{df["open"][i - batch]}"),
                            "close": Decimal(f"{df["close"][i]}"),
                            "count_candles": batch,
                            "time_start": df["time"][i - batch],
                            "time_end": df["time"][i],
                        }
                    )
            elif direction == "UP":  # prev candles
                if batch >= 2:  # Pattern high 1
                    swings.append(
                        {
                            "type": "UP",
                            "level": max(
                                [
                                    Decimal(f"{df["high"][i - 1]}"),
                                    Decimal(f"{df["high"][i - 2]}"),
                                    Decimal(f"{df["high"][i]}"),
                                ]
                            ),
                            "open": Decimal(f"{df["open"][i - batch]}"),
                            "close": Decimal(f"{df["close"][i - 1]}"),
                            "count_candles": batch,
                            "time_start": df["time"][i - batch],
                            "time_end": df["time"][i - 1],
                        }
                    )
                else:  # Pattern high 2
                    levels = [
                        Decimal(f"{df["high"][i - 1]}"),
                        Decimal(f"{df["high"][i]}"),
                    ]
                    if df["high"][i + 1] and Decimal(f"{df["open"][i + 1]}") > Decimal(
                        f"{df["close"][i + 1]}"
                    ):
                        levels.append(Decimal(f"{df["high"][i + 1]}"))
                    swings.append(
                        {
                            "type": "UP",
                            "level": max(levels),
                            "open": Decimal(f"{df["open"][i - batch]}"),
                            "close": Decimal(f"{df["close"][i - 1]}"),
                            "count_candles": batch,
                            "time_start": df["time"][i - batch],
                            "time_end": df["time"][i - 1],
                        }
                    )

                direction = "DOWN"
                batch = 1

            else:  # If it is first element
                direction = "DOWN"
                batch = 1

    return swings
