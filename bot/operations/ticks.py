import MetaTrader5 as mt5


def get_ticks(symbol, time, flags=mt5.COPY_TICKS_ALL):
    ticks = mt5.copy_ticks_range(symbol, time, time, flags)
    ticks["ask"] = ticks["ask"].astype(str)
    ticks["bid"] = ticks["bid"].astype(str)
    return ticks[["time", "ask", "bid"]]
