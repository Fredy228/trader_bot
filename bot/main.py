import MetaTrader5 as mt5
import signal
import sys
import webbrowser
import threading
import traceback

from common.connect import connect
from common.account import output_account_info
from common.symbol import check_symbol
from mode.strategy_1.test_strategy_1 import test_strategy_1
from mode.strategy_1.prod_strategy_1 import prod_strategy_1

from config import MODE

connect()
output_account_info()
check_symbol()


def signal_handler(sig, frame):
    print("\nПрограма зупиняється...")
    print("Виконується відключення від Metatrader 5...")
    mt5.shutdown()
    print("Успішно відключенно. Можна закривати програму.")
    sys.exit(0)


def open_browser():
    webbrowser.open_new("http://localhost:8080")


signal.signal(signal.SIGINT, signal_handler)

try:
    if MODE == "prod":
        app = prod_strategy_1()
        if __name__ == "__main__":
            threading.Timer(1, open_browser).start()
            app.run(host="0.0.0.0", port=8080, debug=False)
    elif MODE == "test":
        app = test_strategy_1()
        if __name__ == "__main__":
            threading.Timer(1, open_browser).start()
            app.run(host="0.0.0.0", port=8080, debug=False)
    else:
        print("\Помилка: невірний режим роботи. Вкажіть 'test' або 'prod'.\n")
        mt5.shutdown()

except Exception as e:
    print("\nПомилка:")
    print(f"{type(e).__name__}: {e}")
    traceback.print_exc()

    mt5.shutdown()
    sys.exit(1)
