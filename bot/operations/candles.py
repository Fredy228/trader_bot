import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import pytz


def get_candles(currency="EURUSD", timeframe=mt5.TIMEFRAME_H1, bars=50):
    rates = mt5.copy_rates_from_pos(currency, timeframe, 0, bars)
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["open"] = df["open"].astype(str)
    df["high"] = df["high"].astype(str)
    df["low"] = df["low"].astype(str)
    df["close"] = df["close"].astype(str)
    return df[["time", "open", "high", "low", "close"]]


def get_candles_from_date(
    currency="EURUSD", timeframe=mt5.TIMEFRAME_H1, from_date=None
):
    date_now = pytz.timezone("Etc/UTC").localize(
        datetime.now().replace(second=0, microsecond=0)
    )
    print("from_date:", from_date)
    print("date_now:", date_now)
    rates = mt5.copy_rates_range(currency, timeframe, from_date, date_now)
    if rates is None or len(rates) == 0:
        raise ValueError("Помилка. Не вдалось отримати свічки.")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["open"] = df["open"].astype(str)
    df["high"] = df["high"].astype(str)
    df["low"] = df["low"].astype(str)
    df["close"] = df["close"].astype(str)
    return df[["time", "open", "high", "low", "close"]]
