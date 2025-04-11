config.py (./bot/config.py)
-------------------------------
import MetaTrader5 as mt5

DEBUG_MODE = 0

SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_H1
BARS = 24

LOGIN = 111111
PASSWORD = "password"
SERVER = "MetaQuotes-Demo"
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
TIMEFRAME_MN1 - 1 месяц
------------------------------
