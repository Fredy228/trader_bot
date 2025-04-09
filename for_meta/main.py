import MetaTrader5 as mt5

from common.connect import connect
from common.account import output_account_info
from operations.candles import get_candles
from operations.extremes import find_extremes
from operations.trend import plot_trend

# LOGIN = 91324930
# PASSWORD = "QfZ@FyG7"
# SERVER = "MetaQuotes-Demo"
# if not mt5.initialize(login=LOGIN, password=PASSWORD, server=SERVER):

connect()

output_account_info()

print("\nGetting data...\n")
df = get_candles("EURUSD", mt5.TIMEFRAME_H1, 24)

# print("candles:\n", df)

print("\nFinding extremes...\n")
swings = find_extremes(df=df)
# pprint(swings)

print("\nTrend analysis...\n")
hours_line, values_line = plot_trend(swings=swings)

print(hours_line)
print(values_line)

mt5.shutdown()
