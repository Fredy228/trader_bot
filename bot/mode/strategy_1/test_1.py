from services.logger import logger
from operations.candles import get_candles_from_date
from trade.trade_test_1 import trade_test_1
from operations.show_static_statistic import show_static_statistic
from operations.transaction import get_time_line_balance

from config import (
    SYMBOL,
    TIMEFRAME,
    FROM_DATE,
)

_has_shown = False


def test_1():
    global _has_shown
    if _has_shown:
        return
    _has_shown = True

    logger.info("Йде отримання даних...")
    print("\nЙде отримання даних...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    len_df = len(df)
    print(f"Отримано {len_df} свічок\n")
    logger.info(f"Отримано {len_df} свічок")

    print("\nЙде торгівля...\n")
    logger.info("Йде торгівля...")
    trend, markers = trade_test_1(df)

    print("\nЙде будування графіку...\n")
    logger.info("Йде будування графіку...")
    balance_history = get_time_line_balance()
    show_static_statistic(
        df,
        trend=trend,
        markers=markers,
        balance_history=balance_history,
    )
