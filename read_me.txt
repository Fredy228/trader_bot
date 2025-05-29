version - 2.1.1

config.py (./bot/config.py)
-------------------------------
import MetaTrader5 as mt5
from datetime import datetime
import pytz

# BASE SETTINGS
DEBUG_MODE = 0  # 1 - on, 0 - off
MODE = "test"  # "test" or "prod"

STRATEGY = 1
SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1
TAKE_PROFIT_DEVIATION = 0  # Значення в відсотках, може бути від'ємне
STOP_LOSS_DEVIATION = 0  # Значення в відсотках, може бути від'ємне
BREAK_TREND_BY = "body"  # "extreme" or "body"

# TESTING SETTINGS
START_BALANCE = 25000
FROM_DATE = datetime(
    2025, 4, 20, 0, 0, tzinfo=pytz.timezone("Etc/UTC")
)  # YYYY, MM, DD, HH, MM

# PRODUCTION SETTINGS
BARS = 60
-------------------------------
Список доступных таймфреймов:

TIMEFRAME_M1 - 1 минута
TIMEFRAME_M2 - 2 минуты
TIMEFRAME_M3 - 3 минуты
TIMEFRAME_M4 - 4 минуты
TIMEFRAME_M5 - 5 минут
TIMEFRAME_M6 - 6 минут
TIMEFRAME_M10 - 10 минут
TIMEFRAME_M12 - 12 минут
TIMEFRAME_M15 - 15 минут
TIMEFRAME_M20 - 20 минут
TIMEFRAME_M30 - 30 минут
TIMEFRAME_H1 - 1 час
TIMEFRAME_H2 - 2 часа
TIMEFRAME_H3 - 3 часа
TIMEFRAME_H4 - 4 часа
TIMEFRAME_H6 - 6 часов
TIMEFRAME_H8 - 8 часов
TIMEFRAME_H12 - 12 часов
TIMEFRAME_D1 - 1 день
TIMEFRAME_W1 - 1 неделя
------------------------------
