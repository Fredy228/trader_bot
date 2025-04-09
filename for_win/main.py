import MetaTrader5 as mt5
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from connect import connect
from account import output_account_info
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

# print(hours_line)
# print(values_line)

print("\nCreating graphic...\n")
fig, ax = plt.subplots()

ax.plot(hours_line, values_line)
ax.set_xticks(hours_line)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

fig.autofmt_xdate()

plt.xlabel("Hour")
plt.ylabel("Value")
plt.title("Анализ тренда")
plt.grid()
plt.show()

mt5.shutdown()
