import MetaTrader5 as mt5
import pandas as pd

from services.logger import logger


def get_ticks(symbol, time_from, time_to, flags=mt5.COPY_TICKS_ALL):
    ticks = mt5.copy_ticks_range(symbol, time_from, time_to, flags)

    if ticks is None or len(ticks) == 0:
        logger.warning(f"Не вдалось отримати тіки. {time_from} - {time_to}")
        return None

    ticks_frame = pd.DataFrame(ticks)
    ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

    ticks_frame["ask"] = ticks_frame["ask"].astype(str)
    ticks_frame["bid"] = ticks_frame["bid"].astype(str)
    return ticks_frame[["time", "ask", "bid"]]
