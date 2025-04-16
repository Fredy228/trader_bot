from pprint import pprint
import plotly.graph_objects as go

from operations.candles import get_candles_from_date
from operations.extremes import find_extremes
from operations.trend import plot_trend

from config import SYMBOL, TIMEFRAME, FROM_DATE, DEBUG_MODE


def test_strategy_1():
    print("\nИдет получение данных...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    if DEBUG_MODE == 1:
        print("candles:\n", df)

    for i in range(2, len(df)):
        gap = df[0 : i + 1] if i <= 60 else df[i - 60 : i + 1]

        swings = find_extremes(df=gap)
        pprint(swings)
