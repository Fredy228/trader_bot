import MetaTrader5 as mt5
import sys

from config import SYMBOL


def check_symbol():
    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        print(f"\nСимвол {SYMBOL} не найден в Metatrader.\n")
        mt5.shutdown()
        sys.exit(1)
