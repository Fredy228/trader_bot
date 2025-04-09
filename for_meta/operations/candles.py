import MetaTrader5 as mt5
import pandas as pd


def get_candles(currency="EURUSD", timeframe=mt5.TIMEFRAME_H1, bars=50):
    rates = mt5.copy_rates_from_pos(currency, timeframe, 0, bars)
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["open"] = df["open"].astype(str)
    df["high"] = df["high"].astype(str)
    df["low"] = df["low"].astype(str)
    df["close"] = df["close"].astype(str)
    return df[["time", "open", "high", "low", "close"]]
