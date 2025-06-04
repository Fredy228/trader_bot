import MetaTrader5 as mt5
import signal
import sys
import traceback

from common.connect import connect
from common.account import output_account_info
from common.symbol import check_symbol
from mode.strategy_1.test_1 import test_1
from mode.strategy_1.prod_strategy_1 import prod_strategy_1
from services.logger import init_logging, logger

from config import (
    TIMEFRAME,
    MODE,
    SYMBOL,
    TAKE_PROFIT_DEVIATION,
    STOP_LOSS_DEVIATION,
    BREAK_TREND_BY,
)

if __name__ == "__main__":
    init_logging()

    logger.info("Запуск програми...")
    print("Запуск програми...")

    connect()
    output_account_info()
    check_symbol()
    logger.info(f"SYMBOL: {SYMBOL}")
    logger.info(f"Timeframe: {TIMEFRAME}")
    logger.info(f"TAKE_PROFIT_DEVIATION: {TAKE_PROFIT_DEVIATION}")
    logger.info(f"STOP_LOSS_DEVIATION: {STOP_LOSS_DEVIATION}")
    logger.info(f"BREAK_TREND_BY: {BREAK_TREND_BY}")

    def signal_handler(sig, frame):
        logger.info("Програма зупинена.")
        print("\nПрограма зупиняється...")
        print("Виконується відключення від Metatrader 5...")
        mt5.shutdown()
        print("Успішно відключенно. Можна закривати програму.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        if MODE == "prod":
            prod_strategy_1()
        elif MODE == "test":
            test_1()
        else:
            print("\Помилка: невірний режим роботи. Вкажіть 'test' або 'prod'.\n")
            mt5.shutdown()

    except Exception as e:
        print("\nПомилка:")
        print(f"{type(e).__name__}: {e}")
        logger.error(f"{type(e).__name__}: {e}")
        traceback.print_exc()

        mt5.shutdown()
        sys.exit(1)

    finally:
        print("Виконується відключення від Metatrader 5...")
        mt5.shutdown()
