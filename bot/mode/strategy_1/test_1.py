from services.logger import logger
from operations.candles import get_candles_from_date
from operations.trade_test_1 import trade_test_1

from config import (
    SYMBOL,
    TIMEFRAME,
    FROM_DATE,
)


def test_1():
    logger.info("Йде отримання даних...")
    print("\nЙде отримання даних...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    len_df = len(df)
    print(f"Отримано {len_df} свічок\n")
    logger.info(f"Отримано {len_df} свічок")

    print("\nЙде торгівля...\n")
    logger.info("Йде торгівля...")
    trade_test_1(df)
