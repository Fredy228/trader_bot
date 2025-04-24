import MetaTrader5 as mt5
import pandas as pd


def get_ticks(symbol, time_from, time_prev, flags=mt5.COPY_TICKS_ALL):
    delta = time_from - time_prev
    time_to = time_from + delta
    ticks = mt5.copy_ticks_range(symbol, time_from, time_to, flags)

    ticks_frame = pd.DataFrame(ticks)
    ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

    ticks_frame["ask"] = ticks_frame["ask"].astype(str)
    ticks_frame["bid"] = ticks_frame["bid"].astype(str)
    return ticks_frame[["time", "ask", "bid"]]
