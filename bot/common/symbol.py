import MetaTrader5 as mt5
import sys

from services.logger import logger
from config import SYMBOL


def check_symbol():
    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        logger.error(f"Символ {SYMBOL} не знайдено в Metatrader.")
        print(f"\nСимвол {SYMBOL} не знайдено в Metatrader.\n")
        logger.error(mt5.last_error())
        mt5.shutdown()
        sys.exit(1)
