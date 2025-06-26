import MetaTrader5 as mt5
from datetime import datetime
import pytz
import pandas as pd

from common.connect import connect

from config import SYMBOL

connect()

time_from = datetime(
    2025, 5, 27, 10, 0, tzinfo=pytz.timezone("Etc/UTC")
)  # YYYY, MM, DD, HH, MM

time_to = datetime(
    2025, 5, 27, 11, 0, tzinfo=pytz.timezone("Etc/UTC")
)  # YYYY, MM, DD, HH, MM

ticks = mt5.copy_ticks_range(SYMBOL, time_from, time_to, mt5.COPY_TICKS_ALL)

if ticks is None or len(ticks) == 0:
    print(f"Не вдалось отримати тіки. {time_from} - {time_to}")

ticks_frame = pd.DataFrame(ticks)
ticks_frame["time"] = pd.to_datetime(ticks_frame["time"], unit="s")

print(ticks_frame)


mt5.shutdown()
