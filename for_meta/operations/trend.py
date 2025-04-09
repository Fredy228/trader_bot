def plot_trend(swings):
    time_line = []
    values_line = []
    level_up = 0
    level_down = 0

    # for i in range(0, len(swings)):
    for i, swing in enumerate(swings):
        curr_level = swing["level"]
        curr_time_start = swing["time_start"]
        curr_time_end = swing["time_end"]
        is_up = swing["type"] == "UP"

        if i == 0:  # fist el
            if is_up:
                level_up = curr_level
            else:
                level_down = curr_level

            time_line.append(curr_time_start)
            values_line.append(curr_level)
        elif i == len(swings) - 1:  # last el
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

    return time_line, values_line

#    new_trend = "UP \u2191"
#    new_trend = "DOWN \u2193"
