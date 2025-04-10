import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pprint import pprint

from common.connect import connect
from common.account import output_account_info
from operations.candles import get_candles
from operations.extremes import find_extremes
from operations.trend import plot_trend

from config import SYMBOL, BARS, TIMEFRAME, METATRADER_MODE, DEBUG_MODE

connect()

output_account_info()

print("\nGetting data...\n")
df = get_candles(SYMBOL, TIMEFRAME, BARS)
if DEBUG_MODE == 1: print("candles:\n", df)

print("\nFinding extremes...\n")
swings = find_extremes(df=df)
if DEBUG_MODE == 1: pprint(swings)

print("\nTrend analysis...\n")
hours_line, values_line = plot_trend(swings=swings)

if METATRADER_MODE == 0:
    print("\nCreating graphic...\n")
    fig, ax = plt.subplots()

    ax.plot(hours_line, values_line)
    ax.set_xticks(hours_line)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    fig.autofmt_xdate()

    plt.xlabel("Hour")
    plt.ylabel("Value")
    plt.title(f"Анализ тренда: {SYMBOL}")
    plt.grid()
    plt.show()

mt5.shutdown()
