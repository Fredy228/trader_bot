def trade_by_trend(swings, candle):
    level_up = 0
    level_down = 0
    time_line = []
    values_line = []

    if len(swings) < 2:
        return

    for i in range(0, len(swings) - 1):
        curr_level = swings[i]["level"]
        curr_time_start = swings[i]["time_start"]
        curr_time_end = swings[i]["time_end"]
        curr_batch = swings[i]["bacth"]
        curr_indexes = swings[i]["indexes"]
        is_up = swings[i]["type"] == "UP"

        if i == 0:  # fist el
            if is_up:
                level_up = curr_level
                values_line.append(
                    candle["low"] if swings[i]["count_candles"] > 1 else candle["high"]
                )

            else:
                level_down = curr_level
                values_line.append(
                    candle["high"] if swings[i]["count_candles"] > 1 else candle["low"]
                )

            time_line.append(curr_time_start)
        elif i == len(swings) - 1:  # last el
            # Logic for trade
            time_line.append(curr_time_end)
            values_line.append(curr_level)
        else:  # middle el
            if is_up:  # UP
                if level_up == 0 or level_up < curr_level:  # Price broke line UP
                    time_line.append(curr_time_end)
                    values_line.append(curr_level)
                    level_up = curr_level
                    level_down = swings[i - 1]["level"]
            else:  # DOWN
                if level_down == 0 or level_down > curr_level:  # Price broke line DOWN
                    time_line.append(curr_time_end)
                    values_line.append(curr_level)
                    level_down = curr_level
                    level_up = swings[i - 1]["level"]
