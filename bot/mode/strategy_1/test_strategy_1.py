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
