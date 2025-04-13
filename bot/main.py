import MetaTrader5 as mt5
import signal
import sys

from common.connect import connect
from common.account import output_account_info
from operations.candles import get_candles
from operations.extremes import find_extremes
from operations.trend import plot_trend
from mode.strategy_1.test_strategy_1 import test_strategy_1
from mode.strategy_1.prod_strategy_1 import prod_strategy_1

from config import MODE, DEBUG_MODE

connect()

output_account_info()


def signal_handler(sig, frame):
    print("\nПрограмма остановливается... \nВыполняем отключение от Metatrader 5...")
    mt5.shutdown()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if MODE == "prod":
    app = prod_strategy_1()
    if __name__ == "__main__":
        app.run(debug=DEBUG_MODE == 1)
elif MODE == "test":
    test_strategy_1()
    mt5.shutdown()
else:
    print("Ошибка: неверный режим работы. Укажите 'test' или 'prod'.")
    mt5.shutdown()
